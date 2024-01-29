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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CloneTLSCertificateTestCase(
    GmpCloneTLSCertificateTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreateTLSCertificateTestCase(
    GmpCreateTLSCertificateTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeleteTLSCertificateTestCase(
    GmpDeleteTLSCertificateTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetTLSCertificateTestCase(
    GmpGetTLSCertificateTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetTLSCertificatesTestCase(
    GmpGetTLSCertificatesTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyTLSCertificateTestCase(
    GmpModifyTLSCertificateTestMixin, Gmpv214TestCase
):
    pass
