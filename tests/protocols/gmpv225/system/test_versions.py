# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.versions import GmpGetVersionTestCase
from ...gmpv225 import Gmpv225TestCase
from .versions import GmpGetProtocolVersionTestCase


class Gmpv225GetVersionCommandTestCase(GmpGetVersionTestCase, Gmpv225TestCase):
    pass


class Gmpv225GmpGetProtocolVersionTestCase(
    GmpGetProtocolVersionTestCase, Gmpv225TestCase
):
    pass
