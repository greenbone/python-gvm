# -*- coding: utf-8 -*-
# Copyright (C) 2018 - 2020 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import warnings

from pathlib import Path

import toml

from packaging.version import Version, InvalidVersion


def deprecation(message: str):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def safe_version(version: str) -> str:
    """
    Returns the version as a string in `PEP440`_ compliant
    format.

    .. _PEP440:
       https://www.python.org/dev/peps/pep-0440
    """
    try:
        return str(Version(version))
    except InvalidVersion:
        version = version.replace(' ', '.')
        return re.sub('[^A-Za-z0-9.]+', '-', version)


def get_version_from_pyproject_toml() -> str:
    """
    Return the version information from the [tool.poetry] section of the
    pyproject.toml file. The version may be in non standardized form.
    """
    path = Path(__file__)
    pyproject_toml_path = path.parent.parent / 'pyproject.toml'

    if not pyproject_toml_path.exists():
        raise RuntimeError('pyproject.toml file not found.')

    pyproject_toml = toml.loads(pyproject_toml_path.read_text())
    if 'tool' in pyproject_toml and 'poetry' in pyproject_toml['tool']:
        return pyproject_toml['tool']['poetry']['version']

    raise RuntimeError('Version information not found in pyproject.toml file.')


def get_version_string(version: tuple) -> str:
    """Create a version string from a version tuple

    Arguments:
        version: version as tuple e.g. (1, 2, 0, dev, 5)

    Returns:
        The version tuple converted into a string representation
    """
    if len(version) > 4:
        ver = ".".join(str(x) for x in version[:4])
        ver += str(version[4])

        if len(version) > 5:
            # support (1, 2, 3, 'beta', 2, 'dev', 1)
            ver += ".{0}{1}".format(str(version[5]), str(version[6]))

        return ver
    else:
        return ".".join(str(x) for x in version)
