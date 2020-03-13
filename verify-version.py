# -*- coding: utf-8 -*-
# Copyright (C) 2020 Greenbone Networks GmbH
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

import sys

from gvm import get_version


def strip_version(version: str) -> str:
    if not version:
        return version

    if version[0] == 'v':
        return version[1:]


def main():
    if len(sys.argv) < 2:
        sys.exit('Missing argument for version.')
        return

    p_version = strip_version(sys.argv[1])
    version = get_version()
    if p_version != version:
        sys.exit(
            "Provided version: {} does not match the python-gvm "
            "version: {}".format(p_version, version)
        )


if __name__ == '__main__':
    main()
