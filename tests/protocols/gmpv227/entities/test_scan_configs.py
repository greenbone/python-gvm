# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.scan_configs import (
    GmpCloneScanConfigTestMixin,
    GmpCreateScanConfigTestMixin,
    GmpDeleteScanConfigTestMixin,
    GmpGetScanConfigsTestMixin,
    GmpGetScanConfigTestMixin,
    GmpImportScanConfigTestMixin,
    GmpModifyScanConfigSetCommentTestMixin,
    GmpModifyScanConfigSetFamilySelectionTestMixin,
    GmpModifyScanConfigSetNameTestMixin,
    GmpModifyScanConfigSetNvtPreferenceTestMixin,
    GmpModifyScanConfigSetNvtSelectionTestMixin,
    GmpModifyScanConfigSetScannerPreferenceTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPCloneScanConfigTestCase(GmpCloneScanConfigTestMixin, GMPTestCase):
    pass


class GMPCreateScanConfigTestCase(GmpCreateScanConfigTestMixin, GMPTestCase):
    pass


class GMPDeleteScanConfigTestCase(GmpDeleteScanConfigTestMixin, GMPTestCase):
    pass


class GMPGetScanConfigTestCase(GmpGetScanConfigTestMixin, GMPTestCase):
    pass


class GMPGetScanConfigsTestCase(GmpGetScanConfigsTestMixin, GMPTestCase):
    pass


class GMPImportScanConfigTestCase(GmpImportScanConfigTestMixin, GMPTestCase):
    pass


class GMPModifyScanConfigSetCommentTestCase(
    GmpModifyScanConfigSetCommentTestMixin, GMPTestCase
):
    pass


class GMPModifyScanConfigSetFamilySelectionTestCase(
    GmpModifyScanConfigSetFamilySelectionTestMixin, GMPTestCase
):
    pass


class GMPModifyScanConfigSetNvtSelectionTestCase(
    GmpModifyScanConfigSetNvtSelectionTestMixin, GMPTestCase
):
    pass


class GMPModifyScanConfigSetNameTestCase(
    GmpModifyScanConfigSetNameTestMixin, GMPTestCase
):
    pass


class GMPModifyScanConfigSetNvtPreferenceTestCase(
    GmpModifyScanConfigSetNvtPreferenceTestMixin, GMPTestCase
):
    pass


class GMPModifyScanConfigSetScannerPreferenceTestCase(
    GmpModifyScanConfigSetScannerPreferenceTestMixin, GMPTestCase
):
    pass
