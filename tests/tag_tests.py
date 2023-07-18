"""
tests/tag_tests.py

This script contains tests for pythonedaartifactinfrastructurebase/tag.py

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
import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

from pythonedaartifactinfrastructurebase.tag import Tag
from pythonedaartifacteventgittagging.tag_created import TagCreated
from pythonedasharedgit.git_repo import GitRepo

import asyncio
import pytest
import unittest

class TagTests(unittest.IsolatedAsyncioTestCase):
    """
    Defines tests for pythonedaartifactinfrastructurebase/tag.py.

    Class name: TagTests

    Responsibilities:
        - Validates the functionality of the Tag class.

    Collaborators:
        - Tag: Some sample instances of a derived class are used in the tests.
    """

    async def test_listen_TagCreated(self):
        """
        Tests the behavior of listen_TagCreated(event).
        """
        # given
        input = TagCreated("https://github.com/pythoneda/base", "main")

        # when
        result = await Tag.listen_TagCreated(input)

        # then
        assert result is not None
        assert type(result) == TagCreated
        assert result.repository_url == "https://github.com/pythoneda-infrastructure/base"
        assert GitRepo.tag_exists(result.repository_url, result.name)

if __name__ == '__main__':
    unittest.main()
