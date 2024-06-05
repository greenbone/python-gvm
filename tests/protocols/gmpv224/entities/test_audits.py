# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .audits import (
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


class Gmpv224CloneAuditTestCase(GmpCloneAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateAuditTestCase(GmpCreateAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DeleteAuditTestCase(GmpDeleteAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetAuditTestCase(GmpGetAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetAuditsTestCase(GmpGetAuditsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyAuditTestCase(GmpModifyAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ResumeAuditTestCase(GmpResumeAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224StartAuditTestCase(GmpStartAuditTestMixin, Gmpv224TestCase):
    pass


class Gmpv224StopAuditTestCase(GmpStopAuditTestMixin, Gmpv224TestCase):
    pass
