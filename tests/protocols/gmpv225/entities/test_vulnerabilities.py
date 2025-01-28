# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.vulnerabilities import (
    GmpGetVulnerabilitiesTestMixin,
    GmpGetVulnerabilityTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225GetVulnerabilityTestCase(
    GmpGetVulnerabilityTestMixin, GMPTestCase
):
    pass


class Gmpv225GetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestMixin, GMPTestCase
):
    pass
