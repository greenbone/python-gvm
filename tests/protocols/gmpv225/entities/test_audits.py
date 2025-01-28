# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.audits import (
    GmpCloneAuditTestMixin,
    GmpCreateAuditTestMixin,
    GmpDeleteAuditTestMixin,
    GmpGetAuditsTestMixin,
    GmpGetAuditTestMixin,
    GmpModifyAuditTestMixin,
    GmpResumeAuditTestMixin,
    GmpStartAuditTestMixin,
    GmpStopAuditTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225CloneAuditTestCase(GmpCloneAuditTestMixin, GMPTestCase):
    pass


class Gmpv225CreateAuditTestCase(GmpCreateAuditTestMixin, GMPTestCase):
    pass


class Gmpv225DeleteAuditTestCase(GmpDeleteAuditTestMixin, GMPTestCase):
    pass


class Gmpv225GetAuditTestCase(GmpGetAuditTestMixin, GMPTestCase):
    pass


class Gmpv225GetAuditsTestCase(GmpGetAuditsTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyAuditTestCase(GmpModifyAuditTestMixin, GMPTestCase):
    pass


class Gmpv225ResumeAuditTestCase(GmpResumeAuditTestMixin, GMPTestCase):
    pass


class Gmpv225StartAuditTestCase(GmpStartAuditTestMixin, GMPTestCase):
    pass


class Gmpv225StopAuditTestCase(GmpStopAuditTestMixin, GMPTestCase):
    pass
