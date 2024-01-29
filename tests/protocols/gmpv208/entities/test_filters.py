# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .filters import (
    GmpCloneFilterTestMixin,
    GmpCreateFilterTestMixin,
    GmpDeleteFilterTestMixin,
    GmpGetFiltersTestMixin,
    GmpGetFilterTestMixin,
    GmpModifyFilterTestMixin,
)


class Gmpv208DeleteFilterTestCase(GmpDeleteFilterTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetFilterTestCase(GmpGetFilterTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetFiltersTestCase(GmpGetFiltersTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneFilterTestCase(GmpCloneFilterTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateFilterTestCase(GmpCreateFilterTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyFilterTestCase(GmpModifyFilterTestMixin, Gmpv208TestCase):
    pass
