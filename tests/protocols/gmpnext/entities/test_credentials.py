# SPDX-FileCopyrightText: 2023-2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from ...gmpv224.entities.credentials import (
    GmpCloneCredentialTestMixin,
    GmpCreateCredentialTestMixin,
    GmpDeleteCredentialTestMixin,
    GmpGetCredentialsTestMixin,
    GmpGetCredentialTestMixin,
    GmpModifyCredentialTestMixin,
)
from ..entities.credentials import (
    GmpCreateActiveDirectoryCredentialTestMixin,
    GmpCreateCredentialStoreCredentialTestMixin,
    GmpModifyActiveDirectoryCredentialTestMixin,
    GmpModifyCredentialStoreCredentialTestMixin,
)


class GMPCloneCredentialTestCase(GmpCloneCredentialTestMixin, GMPTestCase):
    pass


class GMPCreateCredentialTestCase(
    GmpCreateCredentialTestMixin,
    GmpCreateActiveDirectoryCredentialTestMixin,
    GmpCreateCredentialStoreCredentialTestMixin,
    GMPTestCase,
):
    pass


class GMPDeleteCredentialTestCase(GmpDeleteCredentialTestMixin, GMPTestCase):
    pass


class GMPGetCredentialTestCase(GmpGetCredentialTestMixin, GMPTestCase):
    pass


class GMPGetCredentialsTestCase(GmpGetCredentialsTestMixin, GMPTestCase):
    pass


class GMPModifyCredentialTestCase(
    GmpModifyCredentialTestMixin,
    GmpModifyActiveDirectoryCredentialTestMixin,
    GmpModifyCredentialStoreCredentialTestMixin,
    GMPTestCase,
):
    pass
