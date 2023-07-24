#!/usr/bin/env python3
"""
scripts/fix_pythonpath.py

This file defines FixPythonPath class.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythoneda/artifact

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
import importlib
import importlib.util
import logging
import os
from pathlib import Path
import pkgutil
import sys
from typing import Callable, Dict, List

class FixPythonPath():
    """
    A script to rewrite PYTHONPATH to use local repositories.

    Class name: FixPythonPath

    Responsibilities:
        - Analyze sys.path entries.
        - For each entry, check if they are also available in local folder (relative to the current folder)
        - Print the transformed PYTHONPATH to the standard output.

    Collaborators:
        - None
    """

    def __init__(self):
        """
        Initializes the instance.
        """
        super().__init__()

    @classmethod
    def find_modules_under(cls, rootFolder:str) -> List[str]:
        """
        Retrieves the names of the Python modules under given folder.
        :param rootFolder: The root folder.
        :type rootFolder: str
        :return: The list of Python modules.
        :rtype: List[str]
        """
        result = []

        exclude_dirs = {'.git', '__pycache__'}
        for dirpath, dirnames, filenames in os.walk(rootFolder):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs ]
            if '__init__.py' in filenames:
                module = os.path.relpath(dirpath, start=rootFolder)
                if module not in result:
                    result.append(module.replace("/", "."))

        return result

    @classmethod
    def find_modules_under_pythoneda(cls, rootFolder:str) -> List[str]:
        """
        Retrieves the names of the Python modules under given folder.
        :param rootFolder: The root folder.
        :type rootFolder: str
        :return: The list of Python modules.
        :rtype: List[str]
        """
        result = []

        exclude_dirs = {'.git', '__pycache__'}
        for dirpath, dirnames, filenames in os.walk(rootFolder):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs ]
            if '__init__.py' in filenames:
                aux = os.path.relpath(dirpath, start=rootFolder)
                parts = aux.split("/", 2)
                if len(parts) > 2:
                    module = parts[2].replace("/", ".")
                    if module not in result:
                        result.append(module)

        return result

    @classmethod
    def find_path_of_pythoneda_package_with_modules(cls, rootFolder:str, modules:List[str]) -> str:
        """
        Retrieves the path of the package with given modules.
        :param rootFolder: The root folder.
        :type rootFolder: str
        :param modules: The list of modules.
        :type modules: List[str]
        :return: The path.
        :rtype: str
        """
        module_set = set(modules)
        exclude_dirs = {'.git', '__pycache__'}
        _, orgs, _ = next(os.walk(rootFolder))
        orgs[:] = [d for d in orgs if d not in exclude_dirs ]
        for org in orgs:
            org_folder, repos, _ = next(os.walk(Path(rootFolder) / org))
            repos[:] = [d for d in repos if d not in exclude_dirs ]
            for repo in repos:
                current_modules = cls.find_modules_under(Path(org_folder) / repo)
                if set(current_modules) == module_set:
                    return Path(org_folder) / repo

        # If no directory contains all modules, return None
        return None

    @classmethod
    def fix_syspath(cls, rootFolder: str) -> str:
        """
        Fixes the sys.path collection replacing any PythonEDA entries.
        :param rootFolder: The root folder.
        :type rootFolder: str
        :return: The new syspath.
        :rtype: str
        """
        custom_modules = set(cls.find_modules_under_pythoneda(rootFolder))
        paths_to_remove = []
        paths_to_remove.append(Path(__file__).resolve().parent)
        paths_to_add = []
        for path in sys.path:
            modules_under_path = cls.find_modules_under(path)
            if len(modules_under_path) > 0 and all(item in custom_modules for item in modules_under_path):
                paths_to_remove.append(path)
                package_path = cls.find_path_of_pythoneda_package_with_modules(rootFolder, modules_under_path)
                if package_path:
                    paths_to_add.append(package_path)

        for path in paths_to_remove:
            if str(path) in sys.path:
                sys.path.remove(str(path))
        for path in paths_to_add:
            if not str(path) in sys.path:
                sys.path.append(str(path))

    @classmethod
    def print_syspath(cls) -> str:
        """
        Prints the syspath so it can be used to define the PYTHONPATH variable.
        :return: The PYTHONPATH variable.
        :rtype: str
        """
        result = ":".join(sys.path)
        print(result)
        return result

    @classmethod
    def main(cls):
        """
        Runs the application from the command line.
        :param file: The file where this specific instance is defined.
        :type file: str
        """
        cls()
        current_folder = Path(os.getcwd()).resolve()
        root_folder = current_folder.parent.parent
        cls.fix_syspath(root_folder)
        cls.print_syspath()


if __name__ == "__main__":

    FixPythonPath.main()
