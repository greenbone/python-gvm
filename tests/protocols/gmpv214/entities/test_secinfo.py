# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
