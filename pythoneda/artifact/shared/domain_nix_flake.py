# vim: set fileencoding=utf-8
"""
pythoneda/artifact/shared/domain/domain_nix_flake.py

This file defines the DomainNixFlake class.

Copyright (C) 2024-today rydnr's pythoneda-shared-pythonlang-artf/domain

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
from pythoneda.artifact.external.flakeutils import FlakeUtilsNixFlake
from pythoneda.artifact.external.nixpkgs import NixpkgsNixFlake
from pythoneda.artifact.shared.banner import BannerNixFlake
from pythoneda.shared.nix.flake import PythonedaNixFlake
from typing import List


class DomainNixFlake(PythonedaNixFlake):

    """
    Nix flake pythoneda-shared-pythonlang/domain.

    Class name: DomainNixFlake

    Responsibilities:
        - Provides a way to build pythoneda-shared-pythonlang/domain.
        - Provides a way to run pythoneda-shared-pythonlang/domain.

    Collaborators:
        - pythoneda.shared.nix.flake.NixFlake
    """

    def __init__(self, version: str):
        """
        Creates a new DomainNixFlake instance.
        :param version: The version.
        :type version: str
        """
        super().__init__(
            "pythoneda-shared-pythonlang-domain",
            version,
            "github:pythoneda-shared-pythonlang-def/domain/{version}",
            [
                FlakeUtilsNixFlake.default(),
                NixpkgsNixFlake.default(),
                BannerNixFlake.default(),
            ],
            "Support for event-driven architectures in Python",
            "https://github.com/pythoneda-shared-pythonlang/domain",
            "S",
            "D",
            "D",
        )

    @classmethod
    def default(cls):
        """
        Retrieves the default version of the pythoneda-shared/banner Nix flake input.
        :return: Such instance.
        :rtype: pythoneda.artifact.shared.domain.DomainNixFlake
        """
        return cls("0.0.37")


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
