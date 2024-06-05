# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .versions import GmpGetProtocolVersionTestCase, GmpGetVersionTestCase


class Gmpv224GetVersionCommandTestCase(GmpGetVersionTestCase, Gmpv224TestCase):
    pass


class Gmpv224GmpGetProtocolVersionTestCase(
    GmpGetProtocolVersionTestCase, Gmpv224TestCase
):
    pass
