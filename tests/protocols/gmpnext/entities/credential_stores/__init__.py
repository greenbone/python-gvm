#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

from .test_get_credential_stores import GmpGetCredentialStoresTestMixin
from .test_modify_credential_stores import GmpModifyCredentialStoreTestMixin
from .test_verify_credential_stores import GmpVerifyCredentialStoreTestMixin

__all__ = (
    "GmpGetCredentialStoresTestMixin",
    "GmpModifyCredentialStoreTestMixin",
    "GmpVerifyCredentialStoreTestMixin",
)
