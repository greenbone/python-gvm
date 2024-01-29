# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteFilterTestCase(GmpDeleteFilterTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetFilterTestCase(GmpGetFilterTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetFiltersTestCase(GmpGetFiltersTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneFilterTestCase(GmpCloneFilterTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateFilterTestCase(GmpCreateFilterTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyFilterTestCase(GmpModifyFilterTestMixin, Gmpv214TestCase):
    pass
