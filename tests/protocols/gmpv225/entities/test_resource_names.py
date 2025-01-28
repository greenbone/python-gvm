# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv225 import GMPTestCase
from .resourcenames import (
    GmpGetResourceNamesListTestMixin,
    GmpGetResourceNameTestMixin,
)


class Gmpv225GetResourceNamesListTestCase(
    GmpGetResourceNamesListTestMixin, GMPTestCase
):
    pass


class Gmpv225GetResourceNameTestCase(GmpGetResourceNameTestMixin, GMPTestCase):
    pass
