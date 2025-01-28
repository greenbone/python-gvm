# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.schedules import (
    GmpCloneScheduleTestMixin,
    GmpCreateScheduleTestMixin,
    GmpDeleteScheduleTestMixin,
    GmpGetSchedulesTestMixin,
    GmpGetScheduleTestMixin,
    GmpModifyScheduleTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteScheduleTestCase(GmpDeleteScheduleTestMixin, GMPTestCase):
    pass


class Gmpv225GetScheduleTestCase(GmpGetScheduleTestMixin, GMPTestCase):
    pass


class Gmpv225GetSchedulesTestCase(GmpGetSchedulesTestMixin, GMPTestCase):
    pass


class Gmpv225CloneScheduleTestCase(GmpCloneScheduleTestMixin, GMPTestCase):
    pass


class Gmpv225CreateScheduleTestCase(GmpCreateScheduleTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyScheduleTestCase(GmpModifyScheduleTestMixin, GMPTestCase):
    pass
