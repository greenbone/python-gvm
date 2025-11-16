#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later

from .test_create_credential_store_credential import (
    GmpCreateCredentialStoreCredentialTestMixin,
)
from .test_modify_credential_store_credential import (
    GmpModifyCredentialStoreCredentialTestMixin,
)

__all__ = (
    "GmpCreateCredentialStoreCredentialTestMixin",
    "GmpModifyCredentialStoreCredentialTestMixin",
)
