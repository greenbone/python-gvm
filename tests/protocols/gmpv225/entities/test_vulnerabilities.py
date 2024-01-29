# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.vulnerabilities import (
    GmpGetVulnerabilitiesTestMixin,
    GmpGetVulnerabilityTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestMixin, Gmpv225TestCase
):
    pass
