# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.credentials import (
    GmpCloneCredentialTestMixin,
    GmpCreateCredentialTestMixin,
    GmpDeleteCredentialTestMixin,
    GmpGetCredentialsTestMixin,
    GmpGetCredentialTestMixin,
    GmpModifyCredentialTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CloneCredentialTestCase(
    GmpCloneCredentialTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreateCredentialTestCase(
    GmpCreateCredentialTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeleteCredentialTestCase(
    GmpDeleteCredentialTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetCredentialTestCase(GmpGetCredentialTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetCredentialsTestCase(
    GmpGetCredentialsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyCredentialTestCase(
    GmpModifyCredentialTestMixin, Gmpv214TestCase
):
    pass
