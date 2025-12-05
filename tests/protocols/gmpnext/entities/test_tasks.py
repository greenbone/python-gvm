# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
from ...gmpnext import GMPTestCase
from ...gmpnext.entities.tasks import (
    GmpCloneTaskTestMixin,
    GmpCreateAgentGroupTaskTestMixin,
    GmpCreateContainerImageTaskTestMixin,
    GmpCreateContainerTaskTestMixin,
    GmpCreateImportTaskTestMixin,
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


class GMPCloneTaskTestCase(GmpCloneTaskTestMixin, GMPTestCase):
    pass


class GmpCreateAgentGroupTaskTestCase(
    GmpCreateAgentGroupTaskTestMixin, GMPTestCase
):
    pass


class GMPCreateContainerImageTaskTestCase(
    GmpCreateContainerImageTaskTestMixin, GMPTestCase
):
    pass


class GMPCreateContainerTaskTestCase(
    GmpCreateContainerTaskTestMixin, GMPTestCase
):
    pass


class GMPCreateImportTaskTestCase(GmpCreateImportTaskTestMixin, GMPTestCase):
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
