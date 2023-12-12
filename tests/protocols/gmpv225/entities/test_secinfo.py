# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ...gmpv208.entities.secinfo import (
    GmpGetCertBundListTestMixin,
    GmpGetCertBundTestMixin,
    GmpGetCpeListTestMixin,
    GmpGetCpeTestMixin,
    GmpGetCveListTestMixin,
    GmpGetCveTestMixin,
    GmpGetDfnCertListTestMixin,
    GmpGetDfnCertTestMixin,
    GmpGetInfoListTestMixin,
    GmpGetInfoTestMixin,
    GmpGetNvtFamiliesTestMixin,
    GmpGetNvtListTestMixin,
    GmpGetNvtTestMixin,
    GmpGetOvalDefListTestMixin,
    GmpGetOvalDefTestMixin,
    GmpGetScanConfigNvtsTestMixin,
    GmpGetScanConfigNvtTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225GetCertBundTestCase(GmpGetCertBundTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetCpeTestCase(GmpGetCpeTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetCveTestCase(GmpGetCveTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetDfnCertCase(GmpGetDfnCertTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetOvalDefCase(GmpGetOvalDefTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetInfoListTestCase(GmpGetInfoListTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetInfoTestCase(GmpGetInfoTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetNvtTestCase(GmpGetNvtTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetScanConfigNvtTestCase(
    GmpGetScanConfigNvtTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetNvtFamiliesTestCase(
    GmpGetNvtFamiliesTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetScanConfigNvtsTestCase(
    GmpGetScanConfigNvtsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetCertBundListTestCase(
    GmpGetCertBundListTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetCpeListTestCase(GmpGetCpeListTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetCveListTestCase(GmpGetCveListTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetDfnCertListCase(GmpGetDfnCertListTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetNvtListTestCase(GmpGetNvtListTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetOvalDefListTestCase(
    GmpGetOvalDefListTestMixin, Gmpv225TestCase
):
    pass
