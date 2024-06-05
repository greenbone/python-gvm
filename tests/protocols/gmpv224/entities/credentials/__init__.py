# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_credential import GmpCloneCredentialTestMixin
from .test_create_credential import GmpCreateCredentialTestMixin
from .test_delete_credential import GmpDeleteCredentialTestMixin
from .test_get_credential import GmpGetCredentialTestMixin
from .test_get_credentials import GmpGetCredentialsTestMixin
from .test_modify_credential import GmpModifyCredentialTestMixin

__all__ = (
    "GmpCloneCredentialTestMixin",
    "GmpCreateCredentialTestMixin",
    "GmpDeleteCredentialTestMixin",
    "GmpGetCredentialTestMixin",
    "GmpGetCredentialsTestMixin",
    "GmpModifyCredentialTestMixin",
)
