{
  description = "Support for event-driven architectures in Python";
  inputs = rec {
    nixos.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils/v1.0.0";
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixos { inherit system; };
        description = "Support for event-driven architectures in Python";
        license = pkgs.lib.licenses.gpl3;
        homepage = "https://github.com/pythoneda-shared-pythoneda/domain";
        maintainers = [ "rydnr <github@acm-sl.org>" ];
        nixpkgsRelease = "nixos-23.05";
        shared = import ./nix/shared.nix;
        pythoneda-shared-pythoneda-domain-for = { python, version }:
          let
            pname = "pythoneda-shared-pythoneda-domain";
            pnameWithUnderscores =
              builtins.replaceStrings [ "-" ] [ "_" ] pname;
            pythonpackage = "pythoneda";
            pythonVersionParts = builtins.splitVersion python.version;
            pythonMajorVersion = builtins.head pythonVersionParts;
            pythonMajorMinorVersion =
              "${pythonMajorVersion}.${builtins.elemAt pythonVersionParts 1}";
            wheelName =
              "${pnameWithUnderscores}-${version}-py${pythonMajorVersion}-none-any.whl";
          in python.pkgs.buildPythonPackage rec {
            inherit pname version;
            projectDir = ./.;
            scripts = ./scripts;
            pyprojectTemplateFile = ./pyprojecttoml.template;
            pyprojectTemplate = pkgs.substituteAll {
              authors = builtins.concatStringsSep ","
                (map (item: ''"${item}"'') maintainers);
              desc = description;
              inherit homepage pname pythonMajorMinorVersion pythonpackage
                version;
              package = builtins.replaceStrings [ "." ] [ "/" ] pythonpackage;
              src = pyprojectTemplateFile;
            };
            src = pkgs.fetchFromGitHub {
              owner = "pythoneda-shared-pythoneda";
              repo = "domain";
              rev = version;
              sha256 = "sha256-QlToKDJYnotB/n1XuFarvwGESQWoHeF/xmDUuwz6zOQ=";
            };

            format = "pyproject";

            nativeBuildInputs = with python.pkgs; [ pip pkgs.jq poetry-core ];
            propagatedBuildInputs = with python.pkgs; [ ];

            checkInputs = with python.pkgs; [ pytest ];

            pythonImportsCheck = [ pythonpackage ];

            unpackPhase = ''
              cp -r ${src} .
              sourceRoot=$(ls | grep -v env-vars)
              chmod +w $sourceRoot
              cp ${pyprojectTemplate} $sourceRoot/pyproject.toml
            '';

            postInstall = ''
              mkdir $out/dist
              cp -r ${scripts} $out/dist/scripts
              cp dist/${wheelName} $out/dist
              jq ".url = \"$out/dist/${wheelName}\"" $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json > temp.json && mv temp.json $out/lib/python${pythonMajorMinorVersion}/site-packages/${pnameWithUnderscores}-${version}.dist-info/direct_url.json
            '';

            meta = with pkgs.lib; {
              inherit description homepage license maintainers;
            };
          };
        pythoneda-shared-pythoneda-domain-0_0_1a24-for = { python }:
          pythoneda-shared-pythoneda-domain-for {
            version = "0.0.1a24";
            inherit python;
          };
      in rec {
        packages = rec {
          pythoneda-shared-pythoneda-domain-0_0_1a24-python38 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-for {
              python = pkgs.python38;
            };
          pythoneda-shared-pythoneda-domain-0_0_1a24-python39 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-for {
              python = pkgs.python39;
            };
          pythoneda-shared-pythoneda-domain-0_0_1a24-python310 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-for {
              python = pkgs.python310;
            };
          pythoneda-shared-pythoneda-domain-latest-python38 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-python38;
          pythoneda-shared-pythoneda-domain-latest-python39 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-python39;
          pythoneda-shared-pythoneda-domain-latest-python310 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-python310;
          pythoneda-shared-pythoneda-domain-latest =
            pythoneda-shared-pythoneda-domain-latest-python310;
          default = pythoneda-shared-pythoneda-domain-latest;
        };
        defaultPackage = packages.default;
        devShells = rec {
          pythoneda-shared-pythoneda-domain-0_0_1a24-python38 =
            shared.devShell-for {
              package =
                packages.pythoneda-shared-pythoneda-domain-0_0_1a24-python38;
              python = pkgs.python38;
              inherit pkgs nixpkgsRelease;
            };
          pythoneda-shared-pythoneda-domain-0_0_1a24-python39 =
            shared.devShell-for {
              package =
                packages.pythoneda-shared-pythoneda-domain-0_0_1a24-python39;
              python = pkgs.python39;
              inherit pkgs nixpkgsRelease;
            };
          pythoneda-shared-pythoneda-domain-0_0_1a24-python310 =
            shared.devShell-for {
              package =
                packages.pythoneda-shared-pythoneda-domain-0_0_1a24-python310;
              python = pkgs.python310;
              inherit pkgs nixpkgsRelease;
            };
          pythoneda-shared-pythoneda-domain-latest-python38 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-python38;
          pythoneda-shared-pythoneda-domain-latest-python39 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-python39;
          pythoneda-shared-pythoneda-domain-latest-python310 =
            pythoneda-shared-pythoneda-domain-0_0_1a24-python310;
          pythoneda-shared-pythoneda-domain-latest =
            pythoneda-shared-pythoneda-domain-latest-python310;
          default = pythoneda-shared-pythoneda-domain-latest;

        };
      });
}
