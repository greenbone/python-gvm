# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .tls_certificates import (
    GmpCloneTLSCertificateTestMixin,
    GmpCreateTLSCertificateTestMixin,
    GmpDeleteTLSCertificateTestMixin,
    GmpGetTLSCertificatesTestMixin,
    GmpGetTLSCertificateTestMixin,
    GmpModifyTLSCertificateTestMixin,
)


class Gmpv208CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetTLSCertificateTestCase(
    GmpGetTLSCertificateTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestMixin, Gmpv208TestCase
):
    pass
