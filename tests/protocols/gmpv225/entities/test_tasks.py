# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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

from ...gmpv208.entities.tasks import (
    GmpCloneTaskTestMixin,
    GmpCreateContainerTaskTestMixin,
    GmpCreateTaskTestMixin,
    GmpDeleteTaskTestMixin,
    GmpGetTasksTestMixin,
    GmpGetTaskTestMixin,
    GmpModifyTaskTestMixin,
    GmpMoveTaskTestMixin,
    GmpResumeTaskTestMixin,
    GmpStartTaskTestMixin,
    GmpStopTaskTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneTaskTestCase(GmpCloneTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CreateTaskTestCase(GmpCreateTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeleteTaskTestCase(GmpDeleteTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTaskTestCase(GmpGetTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTasksTestCase(GmpGetTasksTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyTaskTestCase(GmpModifyTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225MoveTaskTestCase(GmpMoveTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ResumeTaskTestCase(GmpResumeTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225StartTaskTestCase(GmpStartTaskTestMixin, Gmpv225TestCase):
    pass


class Gmpv225StopTaskTestCase(GmpStopTaskTestMixin, Gmpv225TestCase):
    pass
