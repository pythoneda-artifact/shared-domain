"""
pythonedaartifactinfrastructurebase/tag_created_listener.py

This file declares the TagCreatedListener class.

Copyright (C) 2023-today rydnr's pythoneda-artifact/infrastructure-base

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
from pythonedaartifacteventgittagging.tag_created import TagCreated
from pythonedaartifacteventgittagging.tag_requested import TagRequested
from pythonedasharedgit.git_repo import GitRepo
from typing import List, Type

class TagCreatedListener(EventListener):
    """
    Reacts to TagCreated events for pythoneda-infrastructure/base dependencies.

    Class name: TagCreatedListener

    Responsibilities:
        - Reacts to TagCreated events for pythoneda-infrastructure/base dependencies.

    Collaborators:
        - TagCreated: The event that notifies of a new tag.
        - TagRequested: The event that triggers the tagging process.
    """

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        :return: Such list.
        :rtype: List[Type[Event]]
        """
        return [ TagCreated ]


    @classmethod
    async def listen_TagCreated(cls, event: TagCreated) -> TagRequested:
        """
        Gets notified of a new tag.
        :param event: The TagCreated event.
        :type event: pythonedaartifacteventgittagging.TagCreated
        :return: The request for a new tag, or None.
        :rtype: pythonedaartifacteventgitttagging.tag_requested.TagRequested
        """
        result = None
        if event.repository_url == "https://github.com/pythoneda/base":
            result = TagRequested("https://github.com/pythoneda-artifact/sandbox", "main")
            event_emitter = Ports.instance().resolve(EventEmitter)
            await event_emitter.emit(result)

        return result
