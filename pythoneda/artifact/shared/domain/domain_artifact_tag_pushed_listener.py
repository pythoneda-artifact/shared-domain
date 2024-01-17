# vim: set fileencoding=utf-8
"""
pythoneda/artifact/shared/domain/domain_artifact_tag_pushed_listener.py

This file declares the DomainArtifactTagPushedListener class.

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
import os
from pythoneda.shared import attribute, EventListener
from pythoneda.shared.artifact.artifact.events import (
    ArtifactChangesCommitted,
    ArtifactTagPushed,
)
from pythoneda.shared.artifact.events import Change
from pythoneda.shared.git import (
    GitAdd,
    GitCommit,
    GitRepo,
)


class DomainArtifactTagPushedListener(EventListener):
    """
    Represents how pythoneda-shared-pythoneda/domain-artifact responds to ArtifactTagPushed events.

    Class name: DomainArtifactTagPushedListener

    Responsibilities:
        - Receive ArtifactTagPushed events and react accordingly.

    Collaborators:
        - pythoneda.shared.artifact.events.ArtifactTagPushed
    """

    def __init__(self, repositoryFolder: str):
        """
        Creates a new DomainArtifactTagPushedListener instance.
        :param repositoryFolder: The repository folder.
        :type repositoryFolder: str
        """
        super().__init__()
        self._repository_folder = repositoryFolder

    @property
    @attribute
    def repository_folder(self) -> str:
        """
        Retrieves the repository folder.
        :return: Such folder.
        :rtype: str
        """
        return self._repository_folder

    async def listen(self, event: ArtifactTagPushed) -> ArtifactChangesCommitted:
        """
        Reacts upon given ArtifactTagPushed event to check if affects any of its dependencies.
        In such case, it creates a commit with the dependency change.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.ArtifactTagPushed
        :return: An event representing the commit.
        :rtype: pythoneda.shared.artifact.events.ArtifactChangesCommitted
        """
        result = None
        DomainArtifactTagPushedListener.logger().info(
            f"Checking if {event.name} is one of my inputs"
        )
        dep = next((item.name == event.name for item in self.inputs), None)
        if dep is None:
            DomainArtifactTagPushedListener.logger().info(
                f"Checking if {event.name} is one of my inputs"
            )
        else:
            DomainArtifactTagPushedListener.logger().info(
                f"Updating pythoneda-shared-pythoneda-def/domain since {event.name} updated to version {event.version}"
            )
            # update the affected dependency
            # generate the flake
            self.generate_flake(self.repository_folder)
            # refresh flake.lock
            self.__class__.update_flake_lock(self.repository_folder, "domain")
            # add the change
            git_add = GitAdd(self.repository_folder)
            git_add.add(os.path.join(self.repository_folder, "domain", "flake.nix"))
            git_add.add(os.path.join(self.repository_folder, "domain", "flake.lock"))
            git_add.add(
                os.path.join(self.repository_folder, "domain", "pyproject.toml")
            )
            # commit the change
            commit_hash, commit_diff = GitCommit(self.repository_folder).commit(
                "Updated {dep.name} to {event.version}"
            )
            # generate the ArtifactChangesCommitted event
            result = ArtifactChangesCommitted(
                Change.from_undiff_text(
                    commit_diff,
                    self.url,
                    GitRepo(self.repository_folder).rev,
                    self.repository_folder,
                )
            )
        return result
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
