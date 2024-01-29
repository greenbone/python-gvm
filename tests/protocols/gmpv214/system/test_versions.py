# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.versions import GmpGetVersionTestCase
from ...gmpv214 import Gmpv214TestCase
from .versions import GmpGetProtocolVersionTestCase


class Gmpv214GetVersionCommandTestCase(GmpGetVersionTestCase, Gmpv214TestCase):
    pass


class Gmpv214GmpGetProtocolVersionTestCase(
    GmpGetProtocolVersionTestCase, Gmpv214TestCase
):
    pass
