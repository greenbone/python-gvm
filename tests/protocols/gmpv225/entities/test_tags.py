# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteTagTestCase(GmpDeleteTagTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTagTestCase(GmpGetTagTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetTagsTestCase(GmpGetTagsTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneTagTestCase(GmpCloneTagTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateTagTestCase(GmpCreateTagTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyTagTestCase(GmpModifyTagTestMixin, Gmpv225TestCase):
    pass
