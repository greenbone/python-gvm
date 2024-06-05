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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneAuditTestCase(GmpCloneAuditTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateAuditTestCase(GmpCreateAuditTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeleteAuditTestCase(GmpDeleteAuditTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetAuditTestCase(GmpGetAuditTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetAuditsTestCase(GmpGetAuditsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyAuditTestCase(GmpModifyAuditTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ResumeAuditTestCase(GmpResumeAuditTestMixin, Gmpv225TestCase):
    pass


class Gmpv225StartAuditTestCase(GmpStartAuditTestMixin, Gmpv225TestCase):
    pass


class Gmpv225StopAuditTestCase(GmpStopAuditTestMixin, Gmpv225TestCase):
    pass
