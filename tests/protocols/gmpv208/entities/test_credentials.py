# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .credentials import (
    GmpCloneCredentialTestMixin,
    GmpCreateCredentialTestMixin,
    GmpDeleteCredentialTestMixin,
    GmpGetCredentialsTestMixin,
    GmpGetCredentialTestMixin,
    GmpModifyCredentialTestMixin,
)


class Gmpv208CloneCredentialTestCase(
    GmpCloneCredentialTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CreateCredentialTestCase(
    GmpCreateCredentialTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208DeleteCredentialTestCase(
    GmpDeleteCredentialTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetCredentialTestCase(GmpGetCredentialTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetCredentialsTestCase(
    GmpGetCredentialsTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyCredentialTestCase(
    GmpModifyCredentialTestMixin, Gmpv208TestCase
):
    pass
