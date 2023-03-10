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

from ...gmpv208 import Gmpv208TestCase
from .secinfo import (
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
    GmpGetNvtPreferencesTestMixin,
    GmpGetNvtPreferenceTestMixin,
    GmpGetNvtTestMixin,
    GmpGetOvalDefListTestMixin,
    GmpGetOvalDefTestMixin,
    GmpGetScanConfigNvtsTestMixin,
    GmpGetScanConfigNvtTestMixin,
)


class Gmpv208GetCertBundTestCase(GmpGetCertBundTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetCpeTestCase(GmpGetCpeTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetCveTestCase(GmpGetCveTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetDfnCertCase(GmpGetDfnCertTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetOvalDefCase(GmpGetOvalDefTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetInfoListTestCase(GmpGetInfoListTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetInfoTestCase(GmpGetInfoTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetNvtTestCase(GmpGetNvtTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetNvtPreferenceTestCase(
    GmpGetNvtPreferenceTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetNvtPreferencesTestCase(
    GmpGetNvtPreferencesTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetScanConfigNvtTestCase(
    GmpGetScanConfigNvtTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetNvtFamiliesTestCase(
    GmpGetNvtFamiliesTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetScanConfigNvtsTestCase(
    GmpGetScanConfigNvtsTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetCertBundListTestCase(
    GmpGetCertBundListTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetCpeListTestCase(GmpGetCpeListTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetCveListTestCase(GmpGetCveListTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetDfnCertListCase(GmpGetDfnCertListTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetNvtListTestCase(GmpGetNvtListTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetOvalDefListTestCase(
    GmpGetOvalDefListTestMixin, Gmpv208TestCase
):
    pass
