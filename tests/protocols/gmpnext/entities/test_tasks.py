# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.tasks import (
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
from ...gmpv227 import GMPTestCase


class GMPCloneTaskTestCase(GmpCloneTaskTestMixin, GMPTestCase):
    pass


class GMPCreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, GMPTestCase
):
    pass


class GMPCreateTaskTestCase(GmpCreateTaskTestMixin, GMPTestCase):
    pass


class GMPDeleteTaskTestCase(GmpDeleteTaskTestMixin, GMPTestCase):
    pass


class GMPGetTaskTestCase(GmpGetTaskTestMixin, GMPTestCase):
    pass


class GMPGetTasksTestCase(GmpGetTasksTestMixin, GMPTestCase):
    pass


class GMPModifyTaskTestCase(GmpModifyTaskTestMixin, GMPTestCase):
    pass


class GMPMoveTaskTestCase(GmpMoveTaskTestMixin, GMPTestCase):
    pass


class GMPResumeTaskTestCase(GmpResumeTaskTestMixin, GMPTestCase):
    pass


class GMPStartTaskTestCase(GmpStartTaskTestMixin, GMPTestCase):
    pass


class GMPStopTaskTestCase(GmpStopTaskTestMixin, GMPTestCase):
    pass
