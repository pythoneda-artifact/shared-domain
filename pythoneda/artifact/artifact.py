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
from pythoneda.event import Event
from pythoneda.event_emitter import EventEmitter
from pythoneda.event_listener import EventListener
from pythoneda.ports import Ports
from pythoneda.shared.artifact_changes.events.change_committed import ChangeCommitted
from pythoneda.shared.git.git_repo import GitRepo
from typing import List, Type


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
    async def listen_StagedChangesCommitted(
        cls, event: StagedChangesCommitted
    ) -> CommittedChangesPushed:
        """
        Gets notified of a StagedChangesCommitted event.
        Pushes the changes and emits a CommittedChangesPushed event.
        :param event: The event.
        :type event: pythoneda.realm.rydnr.events.ChangeStagingCodeRequestDelegated
        :return: An event notifying the changes have been pushed.
        :rtype: pythoneda.shared.artifact_changes.events.CommittedChangesPushed
        """
        Domain.logger().debug(f"Received {type(event)}")
        repository_url = GitRepo.remote_urls(event.change.repository_folder)["origin"][
            0
        ]
        # retrieve changes from the cloned repository.
        git_push = GitPush(event.change.repository_folder).push_branch(
            event.change.branch
        )
        result = CommittedChangesPushed(event.repository_url, event.branch, event.id)
        Domain.logger().debug(f"Emitting {type(result)}")
        await Ports.instance().resolve(EventEmitter).emit(result)
        return result
