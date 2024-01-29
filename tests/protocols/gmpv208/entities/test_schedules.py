# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .schedules import (
    GmpCloneScheduleTestMixin,
    GmpCreateScheduleTestMixin,
    GmpDeleteScheduleTestMixin,
    GmpGetSchedulesTestMixin,
    GmpGetScheduleTestMixin,
    GmpModifyScheduleTestMixin,
)


class Gmpv208DeleteScheduleTestCase(
    GmpDeleteScheduleTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetScheduleTestCase(GmpGetScheduleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetSchedulesTestCase(GmpGetSchedulesTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneScheduleTestCase(GmpCloneScheduleTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateScheduleTestCase(
    GmpCreateScheduleTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScheduleTestCase(
    GmpModifyScheduleTestMixin, Gmpv208TestCase
):
    pass
