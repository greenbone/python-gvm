# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.audits import (
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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CloneAuditTestCase(GmpCloneAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateAuditTestCase(GmpCreateAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeleteAuditTestCase(GmpDeleteAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetAuditTestCase(GmpGetAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetAuditsTestCase(GmpGetAuditsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyAuditTestCase(GmpModifyAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ResumeAuditTestCase(GmpResumeAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214StartAuditTestCase(GmpStartAuditTestMixin, Gmpv214TestCase):
    pass


class Gmpv214StopAuditTestCase(GmpStopAuditTestMixin, Gmpv214TestCase):
    pass
