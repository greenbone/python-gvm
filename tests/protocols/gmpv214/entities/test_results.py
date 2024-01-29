# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.results import (
    GmpGetResultsTestMixin,
    GmpGetResultTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214GetResultTestCase(GmpGetResultTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetResultsTestCase(GmpGetResultsTestMixin, Gmpv214TestCase):
    pass
