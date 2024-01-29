# SPDX-FileCopyrightText: 2019-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.protocols.gmpv208 import Gmp

from .. import GmpTestCase


class Gmpv208TestCase(GmpTestCase):
    gmp_class = Gmp
