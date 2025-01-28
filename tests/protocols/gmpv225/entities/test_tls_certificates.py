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
from ...gmpv225 import GMPTestCase


class Gmpv225CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestMixin, GMPTestCase
):
    pass


class Gmpv225CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestMixin, GMPTestCase
):
    pass


class Gmpv225DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestMixin, GMPTestCase
):
    pass


class Gmpv225GetTLSCertificateTestCase(
    GmpGetTLSCertificateTestMixin, GMPTestCase
):
    pass


class Gmpv225GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestMixin, GMPTestCase
):
    pass
