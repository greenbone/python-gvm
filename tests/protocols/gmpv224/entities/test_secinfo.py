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
from ...gmpv224 import Gmpv224TestCase


class Gmpv224GetCertBundTestCase(GmpGetCertBundTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetCpeTestCase(GmpGetCpeTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetCveTestCase(GmpGetCveTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetDfnCertCase(GmpGetDfnCertTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetOvalDefCase(GmpGetOvalDefTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetInfoListTestCase(GmpGetInfoListTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetInfoTestCase(GmpGetInfoTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetNvtTestCase(GmpGetNvtTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetScanConfigNvtTestCase(
    GmpGetScanConfigNvtTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetNvtFamiliesTestCase(
    GmpGetNvtFamiliesTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetScanConfigNvtsTestCase(
    GmpGetScanConfigNvtsTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetCertBundListTestCase(
    GmpGetCertBundListTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetCpeListTestCase(GmpGetCpeListTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetCveListTestCase(GmpGetCveListTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetDfnCertListCase(GmpGetDfnCertListTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetNvtListTestCase(GmpGetNvtListTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetOvalDefListTestCase(
    GmpGetOvalDefListTestMixin, Gmpv224TestCase
):
    pass
