# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.results import (
    GmpGetResultsTestMixin,
    GmpGetResultTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225GetResultTestCase(GmpGetResultTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetResultsTestCase(GmpGetResultsTestMixin, Gmpv225TestCase):
    pass
