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
