# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
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
