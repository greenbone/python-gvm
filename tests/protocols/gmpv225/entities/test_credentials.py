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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneCredentialTestCase(
    GmpCloneCredentialTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CreateCredentialTestCase(
    GmpCreateCredentialTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225DeleteCredentialTestCase(
    GmpDeleteCredentialTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetCredentialTestCase(GmpGetCredentialTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetCredentialsTestCase(
    GmpGetCredentialsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyCredentialTestCase(
    GmpModifyCredentialTestMixin, Gmpv225TestCase
):
    pass
