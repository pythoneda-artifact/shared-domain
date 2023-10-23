"""
pythoneda/artifact/artifact.py

This file declares the Artifact class.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythoneda/domain-artifact

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
from pythoneda import Event, EventEmitter, EventListener, listen, Ports
from pythoneda.shared.artifact_changes.events import ArtifactChangesCommitted, CommittedChangesTagged, StagedChangesCommitted, TagPushed
from pythoneda.shared.git import GitAdd, GitAddFailed, GitCommit, GitCommitFailed, GitPush, GitPushFailed, GitRepo, GitTag, GitTagFailed, Version
import requests

class Artifact(EventListener):
    """
    Reacts to artifact events.

    Class name: Artifact

    Responsibilities:
        - React to StagedChangesCommitted events.

    Collaborators:
        - StagedChangesCommitted
        - CommittedChangesPushed
    """

    def __init__(self):
        """
        Creates a new Artifact instance.
        """
        super().__init__()

    @classmethod
    @listen(StagedChangesCommitted)
    async def listen_StagedChangesCommitted(cls, event: StagedChangesCommitted) -> CommittedChangesTagged:
        """
        Gets notified of a StagedChangesCommitted event.
        Creates a tag and emits a CommittedChangesTagged event.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.StagedChangesCommitted
        :return: An event notifying the commit has been tagged.
        :rtype: pythoneda.shared.artifact_changes.events.CommittedChangesTagged
        """
        result = None
        Artifact.logger().debug(f"Received {type(event)}")
        version = await cls().tag(event.change.repository_folder)
        if version is not None:
            result = CommittedChangesTagged(version.value, event.commit, event.change.repository_url, event.change.branch, event.change.repository_folder, event.id)
            Artifact.logger().debug(f"Emitting {result}")
            await Ports.instance().resolve(EventEmitter).emit(result)
            return result

    def own_flake(self, folder:str) -> bool:
        """
        Checks if the repository has its own flake, so it doesn't have an artifact space.
        :param folder: The repository folder.
        :type folder: str
        :return: True in such case.
        :rtype: bool
        """
        return os.path.exists(os.path.join(folder, "flake.nix"))

    async def tag(self, folder:str) -> Version:
        """
        Creates a tag and emits a CommittedChangesTagged event.
        :param folder: The repository folder.
        :type folder: str
        :return: The tagged version.
        :rtype: pythoneda.shared.git.Version
        """
        git_tag = GitTag(folder)
        git_repo = GitRepo.from_folder(folder)
        result = git_repo.increase_patch(False)
        # check if there's a flake in the root folder.
        if self.own_flake(folder):
            flake = os.path.join(folder, "flake.nix")
            # if there's a flake, change and commit the version change before tagging.
            version_updated = await self.update_version_in_flake(result.value, flake)
            if version_updated:
                # stage the change in the flake.
                GitAdd(folder).add(flake)
                # commit the change in the flake
                GitCommit(folder).commit(f"Updated version to {result.value}")
        try:
            git_repo.tag_version(result)
        except GitTagFailed as err:
            Artifact.logger().error('Could not create tag')
            Artifact.logger().error(err)
            result = None
        return result

    async def update_version_in_flake(self, version:str, flake:str) -> bool:
        """
        Updates the version in given flake file.
        :param version: The new version.
        :type version: str
        :param flake: The flake file.
        :type flake: str
        :return: True if the flake could be updated.
        :rtype: bool
        """
        try:
            subprocess.run(
                ["update-sha256-nix-flake.sh", "-f", flake, "-V", version],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.folder,
            )
        except subprocess.CalledProcessError as err:
            GitPush.logger().error(err.stdout)
            GitPush.logger().error(err.stderr)
            raise GitPushFailed(self.folder)

        return True

    @classmethod
    @listen(CommittedChangesTagged)
    async def listen_CommittedChangesTagged(cls, event: CommittedChangesTagged) -> TagPushed:
        """
        Gets notified of a CommittedChangesTagged event.
        Pushes the changes and emits a CommittedChangesPushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.StagedChangesCommitted
        :return: An event notifying the changes have been pushed.
        :rtype: pythoneda.shared.artifact_changes.events.CommittedChangesPushed
        """
        result = None
        Artifact.logger().debug(f"Received {type(event)}")
        pushed = await cls().push_tags(event.repository_folder)
        if pushed:
            result = TagPushed(event.tag, event.commit, event.repository_url, event.branch, event.repository_folder, event.id)
            Artifact.logger().debug(f"Emitting {type(result)}")
            await Ports.instance().resolve(EventEmitter).emit(result)
        return result

    async def push_tags(self, folder:str) -> bool:
        """
        Pushes the tags in given folder.
        :param folder: The folder.
        :type folder: str
        :return: True if the operation succeeds.
        :rtype: bool
        """
        result = False
        try:
            GitPush(folder).push_tags()
            result = True
        except GitPushFailed as err:
            Artifact.logger().error('Could not push tags')
            Artifact.logger().error(err)
            result = False
        return result

    @classmethod
    @listen(TagPushed)
    async def listen_TagPushed(cls, event: TagPushed) -> ArtifactChangesCommitted:
        """
        Gets notified of a TagPushed event.
        Pushes the changes and emits a TagPushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.TagPushed
        :return: An event notifying the changes in the artifact have been committed.
        :rtype: pythoneda.shared.artifact_changes.events.ArtifactChangesCommitted
        """
        result = None
        Artifact.logger().info(f"Received {event}")
        result = await cls().update_artifact_version(event)
        if result is not None:
            Artifact.logger().debug(f"Emitting {type(result)}")
            await Ports.instance().resolve(EventEmitter).emit(result)
        return result

    async def update_artifact_version(self, event: TagPushed) -> ArtifactChangesCommitted:
        """
        Conditionally updates the artifact version.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.TagPushed
        :return: An event notifying the changes in the artifact have been committed.
        :rtype: pythoneda.shared.artifact_changes.events.ArtifactChangesCommitted
        """
        result = None
        artifact_repo = None
        # check if there's a flake in the root folder.
        if not self.own_flake(event.repository_folder):
            # retrieve the artifact repository, if any.
            artifact_repo = self.artifact_repository_url_for(event.repository_url)

        artifact_repo_folder = None
        if artifact_repo is not None:
            # find out the local folder for the artifact repository
            artifact_repo_folder = self.artifact_repository_folder_of(artifact_repo, event.repository_folder)

        flake = None
        if artifact_repo_folder is not None:
            # retrieve subfolder for the flake
            flake = self.flake_path_in_artifact_repository(artifact_repo_folder, event.repository_url)

        if flake is not None:
            # update the version and hash in the flake of the artifact repository
            if self.update_version_in_flake(Version(event.tag), flake):
                result = ArtifactChangesCommitted(event.tag, event.commit, event.repository_url, event.branch, event.id)

        return result

    def artifact_repository_url_for(self, url:str) -> str:
        """
        Retrieves the url of the artifact repository for given url.
        :param url: The repository url.
        :type url: str
        :return: The url of the artfifact repository, or None if not found.
        :rtype: str
        """
        result = None
        artifact_url = f'{url}-artifact'
        if self.url_exists(artifact_url):
            result = artifact_url

        return result

    def url_exists(self, url:str) -> bool:
        """
        Checks if given url exists.
        :param url: The url to check.
        :type url: str
        :return: True if the url exists.
        :rtype: bool
        """
        result = False
        try:
            response = requests.head(url)
            if response.status_code == 200:
                result = True
        except requests.RequestException as err:
            Artifact.logger().error(f'Could not check if {url} exists')
            Artifact.logger().error(err)

        return result

    def artifact_repository_folder_of(self, artifactRepoUrl:str, domainRepoFolder:str) -> str:
        """
        Retrieves the folder of the artifact repository for the domain repository cloned in given folder.
        :param artifactRepoUrl: The url of the artifact repository.
        :type artifactRepoUrl: str
        :param domainRepoFolder: The folder where the associated domain repository is cloned.
        :type domainRepoFolder: str
        :return: The folder where the artifact repository is cloned, or None if it doesn't exist.
        :rtype: str
        """
        # TODO: make the folder layout flexible and customizable
        result = None
        _, repo = GitRepo.extract_repo_owner_and_repo_name(artifactRepoUrl)
        artifact_repo_folder = os.path.join(os.path.dirname(domainRepoFolder), repo)
        if os.path.exists(artifact_repo_folder) and os.path.isdir(artifact_repo_folder) and os.path.exists(os.path.join(artifact_repo_folder, ".git")):
            result = artifact_repo_folder

        return result

    def flake_path_in_artifact_repository(self, artifactRepoFolder:str, domainRepoUrl:str) -> str:
        """
        Retrieves the path of the domain flake within its artifact repository.
        :param artifactRepoFolder: The folder where the artifact repository is cloned.
        :type artifactRepoFolder: str
        :param domainRepoUrl: The url of the domain repository.
        :type domainRepoUrl: str
        :return: The flake path, or None if not found.
        :rtype: str
        """
        result = None
        _, repo = GitRepo.extract_repo_owner_and_repo_name(domainRepoUrl)
        flake = os.path.join(artifactRepoFolder, repo, "flake.nix")
        if os.path.exists(flake):
            result = flake
        return result
