# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.versions import GmpGetVersionTestCase
from ...gmpv226 import GMPTestCase
from .versions import GmpGetProtocolVersionTestCase


class GMPGetVersionCommandTestCase(GmpGetVersionTestCase, GMPTestCase):
    pass


class GMPGetProtocolVersionTestCase(GmpGetProtocolVersionTestCase, GMPTestCase):
    pass
