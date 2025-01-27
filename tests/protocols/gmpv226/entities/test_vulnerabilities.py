# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.vulnerabilities import (
    GmpGetVulnerabilitiesTestMixin,
    GmpGetVulnerabilityTestMixin,
)
from ...gmpv226 import GMPTestCase


class GMPGetVulnerabilityTestCase(GmpGetVulnerabilityTestMixin, GMPTestCase):
    pass


class GMPGetVulnerabilitiesTestCase(
    GmpGetVulnerabilitiesTestMixin, GMPTestCase
):
    pass
