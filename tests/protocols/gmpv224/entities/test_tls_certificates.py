# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.tls_certificates import (
    GmpCloneTLSCertificateTestMixin,
    GmpCreateTLSCertificateTestMixin,
    GmpDeleteTLSCertificateTestMixin,
    GmpGetTLSCertificatesTestMixin,
    GmpGetTLSCertificateTestMixin,
    GmpModifyTLSCertificateTestMixin,
)
from ...gmpv224 import Gmpv224TestCase


class Gmpv224CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetTLSCertificateTestCase(
    GmpGetTLSCertificateTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestMixin, Gmpv224TestCase
):
    pass
