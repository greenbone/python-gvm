# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_get_cert_bund_advisories import GmpGetCertBundListTestMixin
from .test_get_cert_bund_advisory import GmpGetCertBundTestMixin
from .test_get_cpe import GmpGetCpeTestMixin
from .test_get_cpes import GmpGetCpeListTestMixin
from .test_get_cve import GmpGetCveTestMixin
from .test_get_cves import GmpGetCveListTestMixin
from .test_get_dfn_cert_advisories import GmpGetDfnCertListTestMixin
from .test_get_dfn_cert_advisory import GmpGetDfnCertTestMixin
from .test_get_info import GmpGetInfoTestMixin
from .test_get_info_list import GmpGetInfoListTestMixin
from .test_get_nvt import GmpGetNvtTestMixin
from .test_get_nvt_families import GmpGetNvtFamiliesTestMixin
from .test_get_nvt_preference import GmpGetNvtPreferenceTestMixin
from .test_get_nvt_preferences import GmpGetNvtPreferencesTestMixin
from .test_get_nvts import GmpGetNvtListTestMixin
from .test_get_oval_definition import GmpGetOvalDefTestMixin
from .test_get_oval_definitions import GmpGetOvalDefListTestMixin
from .test_get_scan_config_nvt import GmpGetScanConfigNvtTestMixin
from .test_get_scan_config_nvts import GmpGetScanConfigNvtsTestMixin

__all__ = (
    "GmpGetCertBundListTestMixin",
    "GmpGetCertBundTestMixin",
    "GmpGetCpeTestMixin",
    "GmpGetCpeListTestMixin",
    "GmpGetCveTestMixin",
    "GmpGetCveListTestMixin",
    "GmpGetDfnCertListTestMixin",
    "GmpGetDfnCertTestMixin",
    "GmpGetInfoTestMixin",
    "GmpGetInfoListTestMixin",
    "GmpGetNvtTestMixin",
    "GmpGetNvtFamiliesTestMixin",
    "GmpGetNvtPreferenceTestMixin",
    "GmpGetNvtPreferencesTestMixin",
    "GmpGetNvtListTestMixin",
    "GmpGetOvalDefTestMixin",
    "GmpGetOvalDefListTestMixin",
    "GmpGetScanConfigNvtTestMixin",
    "GmpGetScanConfigNvtsTestMixin",
)
