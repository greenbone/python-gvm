# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .schedules import (
    GmpCloneScheduleTestMixin,
    GmpCreateScheduleTestMixin,
    GmpDeleteScheduleTestMixin,
    GmpGetSchedulesTestMixin,
    GmpGetScheduleTestMixin,
    GmpModifyScheduleTestMixin,
)


class Gmpv224DeleteScheduleTestCase(
    GmpDeleteScheduleTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetScheduleTestCase(GmpGetScheduleTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetSchedulesTestCase(GmpGetSchedulesTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CloneScheduleTestCase(GmpCloneScheduleTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateScheduleTestCase(
    GmpCreateScheduleTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScheduleTestCase(
    GmpModifyScheduleTestMixin, Gmpv224TestCase
):
    pass
