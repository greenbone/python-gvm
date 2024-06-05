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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetTLSCertificateTestCase(
    GmpGetTLSCertificateTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestMixin, Gmpv225TestCase
):
    pass
