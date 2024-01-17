# vim: set fileencoding=utf-8
"""
pythoneda/artifact/shared/domain/domain.py

This file declares the Domain class.

Copyright (C) 2023-today rydnr's pythoneda-artifact/shared-domain

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.shared.artifact import PythonPackage
from pythoneda.shared.nix_flake import (
    FlakeUtilsNixFlake,
    License,
    PythonedaSharedPythonedaBannerNixFlake,
)


class Domain(PythonPackage):
    """
    Represents the pythoneda-shared-pythoneda/domain Python package.

    Class name: Domain

    Responsibilities:
        - Model the pythoneda-shared-pythoneda/domain Python package and its metadata.

    Collaborators:
        - pythoneda.shared.artifact.PythonPackage
    """

    def __init__(self, repositoryFolder: str):
        """
        Creates a new PythonPackage instance.
        :param repositoryFolder: The repository folder.
        :type repositoryFolder: str
        """
        flake_utils = FlakeUtilsNixFlake.default()
        nixos = NixosNixFlake.default()
        banner = PythonedaSharedPythonedaBannerNixFlake.default()
        inputs = [flake_utils, nixos, banner]
        version = self.find_out_version(repositoryFolder)
        super().__init__(
            "pythoneda-shared-pythoneda-domain",
            self.find_out_version(repositoryFolder),
            f"https://github.com/pythoneda-shared-pythoneda/domain-artifact/{version}?dir=domain",
            inputs,
            templateSubfolder,
            "Support for event-driven architectures in Python",
            "https://github.com/pythoneda-shared-pythoneda/domain",
            License.from_id(
                Gpl3.license_type(),
                "2023",
                "rydnr",
                "https://github.com/pythoneda-shared-pythoneda/domain",
            ),
            ["rydnr <github@acm-sl.org>"],
            2023,
            "rydnr",
        )

    @classmethod
    @property
    def url(cls) -> str:
        """
        Retrieves the url.
        :return: Such url.
        :rtype: str
        """
        #        return "https://github.com/pythoneda-shared-pythoneda/domain-artifact"
        return "https://github.com/rydnr/sandbox-artifact"
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
