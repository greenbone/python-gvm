# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.credentials import (
    GmpCloneCredentialTestMixin,
    GmpCreateCredentialTestMixin,
    GmpDeleteCredentialTestMixin,
    GmpGetCredentialsTestMixin,
    GmpGetCredentialTestMixin,
    GmpModifyCredentialTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225CloneCredentialTestCase(GmpCloneCredentialTestMixin, GMPTestCase):
    pass


class Gmpv225CreateCredentialTestCase(
    GmpCreateCredentialTestMixin, GMPTestCase
):
    pass


class Gmpv225DeleteCredentialTestCase(
    GmpDeleteCredentialTestMixin, GMPTestCase
):
    pass


class Gmpv225GetCredentialTestCase(GmpGetCredentialTestMixin, GMPTestCase):
    pass


class Gmpv225GetCredentialsTestCase(GmpGetCredentialsTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyCredentialTestCase(
    GmpModifyCredentialTestMixin, GMPTestCase
):
    pass
