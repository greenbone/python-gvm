# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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

from ...gmpv2110 import Gmpv2110TestCase
from ...gmpv208.entities.secinfo import (
    GmpGetCertBundTestMixin,
    GmpGetCertBundListTestMixin,
    GmpGetCpeTestMixin,
    GmpGetCpeListTestMixin,
    GmpGetCveTestMixin,
    GmpGetCveListTestMixin,
    GmpGetDfnCertTestMixin,
    GmpGetDfnCertListTestMixin,
    GmpGetInfoListTestMixin,
    GmpGetInfoTestMixin,
    GmpGetNvtFamiliesTestMixin,
    GmpGetNvtTestMixin,
    GmpGetNvtListTestMixin,
    GmpGetOvalDefTestMixin,
    GmpGetOvalDefListTestMixin,
    GmpGetScanConfigNvtsTestMixin,
    GmpGetScanConfigNvtTestMixin,
)


class Gmpv2110GetCertBundTestCase(GmpGetCertBundTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetCpeTestCase(GmpGetCpeTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetCveTestCase(GmpGetCveTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetDfnCertCase(GmpGetDfnCertTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetOvalDefCase(GmpGetOvalDefTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetInfoListTestCase(GmpGetInfoListTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetInfoTestCase(GmpGetInfoTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetNvtTestCase(GmpGetNvtTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetScanConfigNvtTestCase(
    GmpGetScanConfigNvtTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110GetNvtFamiliesTestCase(
    GmpGetNvtFamiliesTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110GetScanConfigNvtsTestCase(
    GmpGetScanConfigNvtsTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110GetCertBundListTestCase(
    GmpGetCertBundListTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110GetCpeListTestCase(GmpGetCpeListTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetCveListTestCase(GmpGetCveListTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetDfnCertListCase(GmpGetDfnCertListTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetNvtListTestCase(GmpGetNvtListTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetOvalDefListTestCase(
    GmpGetOvalDefListTestMixin, Gmpv2110TestCase
):
    pass
