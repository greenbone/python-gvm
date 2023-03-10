# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214GetCertBundTestCase(GmpGetCertBundTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetCpeTestCase(GmpGetCpeTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetCveTestCase(GmpGetCveTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetDfnCertCase(GmpGetDfnCertTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetOvalDefCase(GmpGetOvalDefTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetInfoListTestCase(GmpGetInfoListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetInfoTestCase(GmpGetInfoTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetNvtTestCase(GmpGetNvtTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetScanConfigNvtTestCase(
    GmpGetScanConfigNvtTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetNvtFamiliesTestCase(
    GmpGetNvtFamiliesTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetScanConfigNvtsTestCase(
    GmpGetScanConfigNvtsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetCertBundListTestCase(
    GmpGetCertBundListTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetCpeListTestCase(GmpGetCpeListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetCveListTestCase(GmpGetCveListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetDfnCertListCase(GmpGetDfnCertListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetNvtListTestCase(GmpGetNvtListTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetOvalDefListTestCase(
    GmpGetOvalDefListTestMixin, Gmpv214TestCase
):
    pass
