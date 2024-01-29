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
from ...gmpv224 import Gmpv224TestCase


class Gmpv224CloneCredentialTestCase(
    GmpCloneCredentialTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224CreateCredentialTestCase(
    GmpCreateCredentialTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224DeleteCredentialTestCase(
    GmpDeleteCredentialTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetCredentialTestCase(GmpGetCredentialTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetCredentialsTestCase(
    GmpGetCredentialsTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyCredentialTestCase(
    GmpModifyCredentialTestMixin, Gmpv224TestCase
):
    pass
