# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.results import (
    GmpGetResultsTestMixin,
    GmpGetResultTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225GetResultTestCase(GmpGetResultTestMixin, GMPTestCase):
    pass


class Gmpv225GetResultsTestCase(GmpGetResultsTestMixin, GMPTestCase):
    pass
