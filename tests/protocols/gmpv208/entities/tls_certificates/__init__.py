# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_tls_certificate import GmpCloneTLSCertificateTestMixin
from .test_create_tls_certificate import GmpCreateTLSCertificateTestMixin
from .test_delete_tls_certificate import GmpDeleteTLSCertificateTestMixin
from .test_get_tls_certificate import GmpGetTLSCertificateTestMixin
from .test_get_tls_certificates import GmpGetTLSCertificatesTestMixin
from .test_modify_tls_certificate import GmpModifyTLSCertificateTestMixin

__all__ = (
    "GmpCloneTLSCertificateTestMixin",
    "GmpCreateTLSCertificateTestMixin",
    "GmpDeleteTLSCertificateTestMixin",
    "GmpGetTLSCertificateTestMixin",
    "GmpGetTLSCertificatesTestMixin",
    "GmpModifyTLSCertificateTestMixin",
)
