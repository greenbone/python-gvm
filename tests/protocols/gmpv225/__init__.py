# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gvm.protocols.gmpv225 import Gmp

from .. import GmpTestCase


class Gmpv225TestCase(GmpTestCase):
    gmp_class = Gmp
