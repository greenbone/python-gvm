# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
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
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteFilterTestCase(GmpDeleteFilterTestMixin, GMPTestCase):
    pass


class Gmpv225GetFilterTestCase(GmpGetFilterTestMixin, GMPTestCase):
    pass


class Gmpv225GetFiltersTestCase(GmpGetFiltersTestMixin, GMPTestCase):
    pass


class Gmpv225CloneFilterTestCase(GmpCloneFilterTestMixin, GMPTestCase):
    pass


class Gmpv225CreateFilterTestCase(GmpCreateFilterTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyFilterTestCase(GmpModifyFilterTestMixin, GMPTestCase):
    pass
