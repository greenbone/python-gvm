# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .tags import (
    GmpCloneTagTestMixin,
    GmpCreateTagTestMixin,
    GmpDeleteTagTestMixin,
    GmpGetTagsTestMixin,
    GmpGetTagTestMixin,
    GmpModifyTagTestMixin,
)


class Gmpv224DeleteTagTestCase(GmpDeleteTagTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTagTestCase(GmpGetTagTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetTagsTestCase(GmpGetTagsTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CloneTagTestCase(GmpCloneTagTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateTagTestCase(GmpCreateTagTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyTagTestCase(GmpModifyTagTestMixin, Gmpv224TestCase):
    pass
