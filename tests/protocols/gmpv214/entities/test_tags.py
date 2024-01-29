# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.tags import (
    GmpCloneTagTestMixin,
    GmpCreateTagTestMixin,
    GmpDeleteTagTestMixin,
    GmpGetTagsTestMixin,
    GmpGetTagTestMixin,
    GmpModifyTagTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214DeleteTagTestCase(GmpDeleteTagTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTagTestCase(GmpGetTagTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetTagsTestCase(GmpGetTagsTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneTagTestCase(GmpCloneTagTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateTagTestCase(GmpCreateTagTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyTagTestCase(GmpModifyTagTestMixin, Gmpv214TestCase):
    pass
