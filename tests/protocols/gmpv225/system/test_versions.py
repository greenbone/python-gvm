# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.versions import GmpGetVersionTestCase
from ...gmpv225 import GMPTestCase
from .versions import GmpGetProtocolVersionTestCase


class Gmpv225GetVersionCommandTestCase(GmpGetVersionTestCase, GMPTestCase):
    pass


class Gmpv225GmpGetProtocolVersionTestCase(
    GmpGetProtocolVersionTestCase, GMPTestCase
):
    pass
