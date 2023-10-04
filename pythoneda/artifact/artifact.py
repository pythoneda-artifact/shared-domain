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
from pythoneda import Event, EventEmitter, EventListener, listen, Ports
from pythoneda.shared.artifact_changes.events import CommittedChangesPushed, StagedChangesCommitted
from pythoneda.shared.git import GitPush

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

    @classmethod
    @listen(StagedChangesCommitted)
    async def listen_StagedChangesCommitted(cls, event: StagedChangesCommitted) -> CommittedChangesPushed:
        """
        Gets notified of a StagedChangesCommitted event.
        Pushes the changes and emits a CommittedChangesPushed event.
        :param event: The event.
        :type event: pythoneda.realm.rydnr.events.ChangeStagingCodeRequestDelegated
        :return: An event notifying the changes have been pushed.
        :rtype: pythoneda.shared.artifact_changes.events.CommittedChangesPushed
        """
        Artifact.logger().debug(f"Received {type(event)}")
        git_push = GitPush(event.change.repository_folder).push_all()
        result = CommittedChangesPushed(event.change.repository_url, event.change.branch, event.id)
        Artifact.logger().debug(f"Emitting {type(result)}")
        await Ports.instance().resolve(EventEmitter).emit(result)
        return result
