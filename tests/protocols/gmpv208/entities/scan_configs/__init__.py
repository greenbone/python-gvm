# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_scan_config import GmpCloneScanConfigTestMixin
from .test_create_scan_config import GmpCreateScanConfigTestMixin
from .test_create_scan_config_from_osp_scanner import (
    GmpCreateScanConfigFromOSPScannerTestMixin,
)
from .test_delete_scan_config import GmpDeleteScanConfigTestMixin
from .test_get_scan_config import GmpGetScanConfigTestMixin
from .test_get_scan_config_preference import GmpGetScanConfigPreferenceTestMixin
from .test_get_scan_config_preferences import (
    GmpGetScanConfigPreferencesTestMixin,
)
from .test_get_scan_configs import GmpGetScanConfigsTestMixin
from .test_import_scan_config import GmpImportScanConfigTestMixin
from .test_modify_scan_config import GmpModifyScanConfigTestMixin
from .test_modify_scan_config_set_comment import (
    GmpModifyScanConfigSetCommentTestMixin,
)
from .test_modify_scan_config_set_family_selection import (
    GmpModifyScanConfigSetFamilySelectionTestMixin,
)
from .test_modify_scan_config_set_name import (
    GmpModifyScanConfigSetNameTestMixin,
)
from .test_modify_scan_config_set_nvt_preference import (
    GmpModifyScanConfigSetNvtPreferenceTestMixin,
)
from .test_modify_scan_config_set_nvt_selection import (
    GmpModifyScanConfigSetNvtSelectionTestMixin,
)
from .test_modify_scan_config_set_scanner_preference import (
    GmpModifyScanConfigSetScannerPreferenceTestMixin,
)
from .test_sync_scan_config import GmpSyncScanConfigTestMixin

__all__ = (
    "GmpCloneScanConfigTestMixin",
    "GmpCreateScanConfigTestMixin",
    "GmpCreateScanConfigFromOSPScannerTestMixin",
    "GmpDeleteScanConfigTestMixin",
    "GmpGetScanConfigTestMixin",
    "GmpGetScanConfigPreferenceTestMixin",
    "GmpGetScanConfigPreferencesTestMixin",
    "GmpGetScanConfigsTestMixin",
    "GmpImportScanConfigTestMixin",
    "GmpModifyScanConfigTestMixin",
    "GmpModifyScanConfigSetCommentTestMixin",
    "GmpModifyScanConfigSetFamilySelectionTestMixin",
    "GmpModifyScanConfigSetNameTestMixin",
    "GmpModifyScanConfigSetNvtPreferenceTestMixin",
    "GmpModifyScanConfigSetNvtSelectionTestMixin",
    "GmpModifyScanConfigSetScannerPreferenceTestMixin",
    "GmpSyncScanConfigTestMixin",
)
