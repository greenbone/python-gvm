# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv226 import GMPTestCase
from .resourcenames import (
    GmpGetResourceNamesListTestMixin,
    GmpGetResourceNameTestMixin,
)


class GMPGetResourceNamesListTestCase(
    GmpGetResourceNamesListTestMixin, GMPTestCase
):
    pass


class GMPGetResourceNameTestCase(GmpGetResourceNameTestMixin, GMPTestCase):
    pass
