# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .filters import (
    GmpCloneFilterTestMixin,
    GmpCreateFilterTestMixin,
    GmpDeleteFilterTestMixin,
    GmpGetFiltersTestMixin,
    GmpGetFilterTestMixin,
    GmpModifyFilterTestMixin,
)


class Gmpv224DeleteFilterTestCase(GmpDeleteFilterTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetFilterTestCase(GmpGetFilterTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetFiltersTestCase(GmpGetFiltersTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CloneFilterTestCase(GmpCloneFilterTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateFilterTestCase(GmpCreateFilterTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyFilterTestCase(GmpModifyFilterTestMixin, Gmpv224TestCase):
    pass
