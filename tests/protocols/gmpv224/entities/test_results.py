# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.results import (
    GmpGetResultsTestMixin,
    GmpGetResultTestMixin,
)
from ...gmpv224 import Gmpv224TestCase


class Gmpv224GetResultTestCase(GmpGetResultTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetResultsTestCase(GmpGetResultsTestMixin, Gmpv224TestCase):
    pass
