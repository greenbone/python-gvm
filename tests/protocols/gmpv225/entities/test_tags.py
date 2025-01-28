# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.tags import (
    GmpCloneTagTestMixin,
    GmpCreateTagTestMixin,
    GmpDeleteTagTestMixin,
    GmpGetTagsTestMixin,
    GmpGetTagTestMixin,
    GmpModifyTagTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteTagTestCase(GmpDeleteTagTestMixin, GMPTestCase):
    pass


class Gmpv225GetTagTestCase(GmpGetTagTestMixin, GMPTestCase):
    pass


class Gmpv225GetTagsTestCase(GmpGetTagsTestMixin, GMPTestCase):
    pass


class Gmpv225CloneTagTestCase(GmpCloneTagTestMixin, GMPTestCase):
    pass


class Gmpv225CreateTagTestCase(GmpCreateTagTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyTagTestCase(GmpModifyTagTestMixin, GMPTestCase):
    pass
