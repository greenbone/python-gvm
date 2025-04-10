# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv227 import GMPTestCase
from ...gmpv226.entities.resourcenames import (
    GmpGetResourceNamesListTestMixin,
    GmpGetResourceNameTestMixin,
)


class GMPGetResourceNamesListTestCase(
    GmpGetResourceNamesListTestMixin, GMPTestCase
):
    pass


class GMPGetResourceNameTestCase(GmpGetResourceNameTestMixin, GMPTestCase):
    pass
