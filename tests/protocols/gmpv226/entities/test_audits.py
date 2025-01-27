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
from ...gmpv226 import GMPTestCase


class GMPCloneAuditTestCase(GmpCloneAuditTestMixin, GMPTestCase):
    pass


class GMPCreateAuditTestCase(GmpCreateAuditTestMixin, GMPTestCase):
    pass


class GMPDeleteAuditTestCase(GmpDeleteAuditTestMixin, GMPTestCase):
    pass


class GMPGetAuditTestCase(GmpGetAuditTestMixin, GMPTestCase):
    pass


class GMPGetAuditsTestCase(GmpGetAuditsTestMixin, GMPTestCase):
    pass


class GMPModifyAuditTestCase(GmpModifyAuditTestMixin, GMPTestCase):
    pass


class GMPResumeAuditTestCase(GmpResumeAuditTestMixin, GMPTestCase):
    pass


class GMPStartAuditTestCase(GmpStartAuditTestMixin, GMPTestCase):
    pass


class GMPStopAuditTestCase(GmpStopAuditTestMixin, GMPTestCase):
    pass
