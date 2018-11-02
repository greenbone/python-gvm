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


def get_version_string(version):
    """Create a version string from a version tuple

    Arguments:
        version (tuple): version as tuple e.g. (1, 2, 0, dev, 5)

    Returns:
        str: The version tuple converted into a string representation
    """
    if len(version) > 3:
        ver = '.'.join(str(x) for x in version[:4])
        ver += str(version[4])
        return ver
    else:
        return '.'.join(str(x) for x in version)
