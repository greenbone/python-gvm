# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteScheduleTestCase(
    GmpDeleteScheduleTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetScheduleTestCase(GmpGetScheduleTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetSchedulesTestCase(GmpGetSchedulesTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneScheduleTestCase(GmpCloneScheduleTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateScheduleTestCase(
    GmpCreateScheduleTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScheduleTestCase(
    GmpModifyScheduleTestMixin, Gmpv225TestCase
):
    pass
