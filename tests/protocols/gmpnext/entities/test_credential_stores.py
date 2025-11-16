# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from ..entities.credential_stores import (
    GmpGetCredentialStoresTestMixin,
    GmpModifyCredentialStoreTestMixin,
    GmpVerifyCredentialStoreTestMixin,
)


class GMPGetCredentialStoresTest(GmpGetCredentialStoresTestMixin, GMPTestCase):
    pass


class GMPModifyCredentialStoreTest(
    GmpModifyCredentialStoreTestMixin, GMPTestCase
):
    pass


class GMPVerifyCredentialStoreTest(
    GmpVerifyCredentialStoreTestMixin, GMPTestCase
):
    pass
