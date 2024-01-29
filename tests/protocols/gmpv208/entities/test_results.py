# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .results import GmpGetResultsTestMixin, GmpGetResultTestMixin


class Gmpv208GetResultTestCase(GmpGetResultTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetResultsTestCase(GmpGetResultsTestMixin, Gmpv208TestCase):
    pass
