# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .report_tls_certificates.test_get_report_tls_certificates import (
    GmpGetReportTlsCertificatesTestMixin,
)


class GmpGetReportTlsCertificatesTestCase(
    GmpGetReportTlsCertificatesTestMixin, GMPTestCase
):
    pass
