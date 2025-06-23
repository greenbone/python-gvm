# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.tls_certificates import (
    GmpCloneTLSCertificateTestMixin,
    GmpCreateTLSCertificateTestMixin,
    GmpDeleteTLSCertificateTestMixin,
    GmpGetTLSCertificatesTestMixin,
    GmpGetTLSCertificateTestMixin,
    GmpModifyTLSCertificateTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPCloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestMixin, GMPTestCase
):
    pass


class GMPCreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestMixin, GMPTestCase
):
    pass


class GMPDeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestMixin, GMPTestCase
):
    pass


class GMPGetTLSCertificateTestCase(GmpGetTLSCertificateTestMixin, GMPTestCase):
    pass


class GMPGetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestMixin, GMPTestCase
):
    pass


class GMPModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestMixin, GMPTestCase
):
    pass
