# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.protocols.gmp import GMPNext

from .. import GmpTestCase as BaseGMPTestCase


class GMPTestCase(BaseGMPTestCase):
    gmp_class = GMPNext
