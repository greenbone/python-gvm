# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
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


class Gmpv208CloneAuditTestCase(GmpCloneAuditTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateAuditTestCase(GmpCreateAuditTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DeleteAuditTestCase(GmpDeleteAuditTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetAuditTestCase(GmpGetAuditTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetAuditsTestCase(GmpGetAuditsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyAuditTestCase(GmpModifyAuditTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ResumeAuditTestCase(GmpResumeAuditTestMixin, Gmpv208TestCase):
    pass


class Gmpv208StartAuditTestCase(GmpStartAuditTestMixin, Gmpv208TestCase):
    pass


class Gmpv208StopAuditTestCase(GmpStopAuditTestMixin, Gmpv208TestCase):
    pass
