# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gvm.protocols.gmp import GMPv226

from .. import GmpTestCase as BaseGMPTestCase


class GMPTestCase(BaseGMPTestCase):
    gmp_class = GMPv226
