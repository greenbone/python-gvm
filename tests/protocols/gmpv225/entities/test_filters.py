# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.filters import (
    GmpCloneFilterTestMixin,
    GmpCreateFilterTestMixin,
    GmpDeleteFilterTestMixin,
    GmpGetFiltersTestMixin,
    GmpGetFilterTestMixin,
    GmpModifyFilterTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteFilterTestCase(GmpDeleteFilterTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetFilterTestCase(GmpGetFilterTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetFiltersTestCase(GmpGetFiltersTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneFilterTestCase(GmpCloneFilterTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateFilterTestCase(GmpCreateFilterTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyFilterTestCase(GmpModifyFilterTestMixin, Gmpv225TestCase):
    pass
