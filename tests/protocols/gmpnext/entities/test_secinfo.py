# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.secinfo import (
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
    GmpGetScanConfigNvtsTestMixin,
    GmpGetScanConfigNvtTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPGetCertBundTestCase(GmpGetCertBundTestMixin, GMPTestCase):
    pass


class GMPGetCpeTestCase(GmpGetCpeTestMixin, GMPTestCase):
    pass


class GMPGetCveTestCase(GmpGetCveTestMixin, GMPTestCase):
    pass


class GMPGetDfnCertCase(GmpGetDfnCertTestMixin, GMPTestCase):
    pass


class GMPGetInfoListTestCase(GmpGetInfoListTestMixin, GMPTestCase):
    pass


class GMPGetInfoTestCase(GmpGetInfoTestMixin, GMPTestCase):
    pass


class GMPGetNvtTestCase(GmpGetNvtTestMixin, GMPTestCase):
    pass


class GMPGetScanConfigNvtTestCase(GmpGetScanConfigNvtTestMixin, GMPTestCase):
    pass


class GMPGetNvtFamiliesTestCase(GmpGetNvtFamiliesTestMixin, GMPTestCase):
    pass


class GMPGetScanConfigNvtsTestCase(GmpGetScanConfigNvtsTestMixin, GMPTestCase):
    pass


class GMPGetCertBundListTestCase(GmpGetCertBundListTestMixin, GMPTestCase):
    pass


class GMPGetCpeListTestCase(GmpGetCpeListTestMixin, GMPTestCase):
    pass


class GMPGetCveListTestCase(GmpGetCveListTestMixin, GMPTestCase):
    pass


class GMPGetDfnCertListCase(GmpGetDfnCertListTestMixin, GMPTestCase):
    pass


class GMPGetNvtListTestCase(GmpGetNvtListTestMixin, GMPTestCase):
    pass
