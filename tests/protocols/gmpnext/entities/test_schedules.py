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
from ...gmpv227 import GMPTestCase


class GMPDeleteScheduleTestCase(GmpDeleteScheduleTestMixin, GMPTestCase):
    pass


class GMPGetScheduleTestCase(GmpGetScheduleTestMixin, GMPTestCase):
    pass


class GMPGetSchedulesTestCase(GmpGetSchedulesTestMixin, GMPTestCase):
    pass


class GMPCloneScheduleTestCase(GmpCloneScheduleTestMixin, GMPTestCase):
    pass


class GMPCreateScheduleTestCase(GmpCreateScheduleTestMixin, GMPTestCase):
    pass


class GMPModifyScheduleTestCase(GmpModifyScheduleTestMixin, GMPTestCase):
    pass
