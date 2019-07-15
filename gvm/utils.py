# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

import warnings


def deprecation(message: str):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


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
