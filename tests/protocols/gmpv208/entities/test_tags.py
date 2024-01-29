# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .tags import (
    GmpCloneTagTestMixin,
    GmpCreateTagTestMixin,
    GmpDeleteTagTestMixin,
    GmpGetTagsTestMixin,
    GmpGetTagTestMixin,
    GmpModifyTagTestMixin,
)


class Gmpv208DeleteTagTestCase(GmpDeleteTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTagTestCase(GmpGetTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetTagsTestCase(GmpGetTagsTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneTagTestCase(GmpCloneTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateTagTestCase(GmpCreateTagTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyTagTestCase(GmpModifyTagTestMixin, Gmpv208TestCase):
    pass
