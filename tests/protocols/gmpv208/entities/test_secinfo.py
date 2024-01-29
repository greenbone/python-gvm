# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
