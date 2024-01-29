# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.schedules import (
    GmpCloneScheduleTestMixin,
    GmpCreateScheduleTestMixin,
    GmpDeleteScheduleTestMixin,
    GmpGetSchedulesTestMixin,
    GmpGetScheduleTestMixin,
    GmpModifyScheduleTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteScheduleTestCase(
    GmpDeleteScheduleTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetScheduleTestCase(GmpGetScheduleTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetSchedulesTestCase(GmpGetSchedulesTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneScheduleTestCase(GmpCloneScheduleTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateScheduleTestCase(
    GmpCreateScheduleTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScheduleTestCase(
    GmpModifyScheduleTestMixin, Gmpv214TestCase
):
    pass
