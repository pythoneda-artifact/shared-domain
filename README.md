# Artifact space for pythoneda-shared-pythoneda/domain

This is the artifact space for [pythoneda-shared-pythoneda/domain](https://github.com/pythoneda-shared-pythoneda/domain "pythoneda-shared-pythoneda/domain").

## How to declare it in your flake

If you are dealing with meta-artifacts, you'd need to check the latest tag of the (meta)artifact of this (artifact) repository: <https://github.com/pythoneda-shared-pythoneda/domain-artifact-artifact/tags>, and use it instead of the `[version]` placeholder below.

```nix
{
  description = "[..]";
  inputs = rec {
    [..]
    pythoneda-shared-pythoneda-domain-artifact = {
      [optional follows]
      url =
        "github:pythoneda-shared-pythoneda/domain-artifact-artifact/[version]?dir=domain-artifact";
    };
  };
  outputs = [..]
};
```

Should you use another PythonEDA modules, you might want to pin those also used by this project.

Use the specific package depending on your system (one of `flake-utils.lib.defaultSystems`) and Python version:

- `#packages.[system].pythoneda-shared-pythoneda-domain-python38` 
- `#packages.[system].pythoneda-shared-pythoneda-domain-python39` 
- `#packages.[system].pythoneda-shared-pythoneda-domain-python310` 
- `#packages.[system].pythoneda-shared-pythoneda-domain-python311` 

The Nix flake is under the [https://github.com/pythoneda-shared-pythoneda/domain-artifact-artifact/tree/main/domain-artifact](domain-artifact "domain-artifact") folder.
