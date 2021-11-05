# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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

from ...gmpv2110 import Gmpv2110TestCase
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


class Gmpv2110CloneTaskTestCase(GmpCloneTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110CreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110CreateTaskTestCase(GmpCreateTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110DeleteTaskTestCase(GmpDeleteTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetTaskTestCase(GmpGetTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetTasksTestCase(GmpGetTasksTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110ModifyTaskTestCase(GmpModifyTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110MoveTaskTestCase(GmpMoveTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110ResumeTaskTestCase(GmpResumeTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110StartTaskTestCase(GmpStartTaskTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110StopTaskTestCase(GmpStopTaskTestMixin, Gmpv2110TestCase):
    pass
