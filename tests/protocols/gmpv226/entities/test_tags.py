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
from ...gmpv226 import GMPTestCase


class GMPDeleteTagTestCase(GmpDeleteTagTestMixin, GMPTestCase):
    pass


class GMPGetTagTestCase(GmpGetTagTestMixin, GMPTestCase):
    pass


class GMPGetTagsTestCase(GmpGetTagsTestMixin, GMPTestCase):
    pass


class GMPCloneTagTestCase(GmpCloneTagTestMixin, GMPTestCase):
    pass


class GMPCreateTagTestCase(GmpCreateTagTestMixin, GMPTestCase):
    pass


class GMPModifyTagTestCase(GmpModifyTagTestMixin, GMPTestCase):
    pass
