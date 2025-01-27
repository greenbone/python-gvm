# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.results import (
    GmpGetResultsTestMixin,
    GmpGetResultTestMixin,
)
from ...gmpv226 import GMPTestCase


class GMPGetResultTestCase(GmpGetResultTestMixin, GMPTestCase):
    pass


class GMPGetResultsTestCase(GmpGetResultsTestMixin, GMPTestCase):
    pass
