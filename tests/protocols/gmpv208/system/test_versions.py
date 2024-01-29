# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .versions import GmpGetProtocolVersionTestCase, GmpGetVersionTestCase


class Gmpv208GetVersionCommandTestCase(GmpGetVersionTestCase, Gmpv208TestCase):
    pass


class Gmpv208GmpGetProtocolVersionTestCase(
    GmpGetProtocolVersionTestCase, Gmpv208TestCase
):
    pass
