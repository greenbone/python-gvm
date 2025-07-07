# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.filters import (
    GmpCloneFilterTestMixin,
    GmpCreateFilterTestMixin,
    GmpDeleteFilterTestMixin,
    GmpGetFiltersTestMixin,
    GmpGetFilterTestMixin,
    GmpModifyFilterTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPDeleteFilterTestCase(GmpDeleteFilterTestMixin, GMPTestCase):
    pass


class GMPGetFilterTestCase(GmpGetFilterTestMixin, GMPTestCase):
    pass


class GMPGetFiltersTestCase(GmpGetFiltersTestMixin, GMPTestCase):
    pass


class GMPCloneFilterTestCase(GmpCloneFilterTestMixin, GMPTestCase):
    pass


class GMPCreateFilterTestCase(GmpCreateFilterTestMixin, GMPTestCase):
    pass


class GMPModifyFilterTestCase(GmpModifyFilterTestMixin, GMPTestCase):
    pass
