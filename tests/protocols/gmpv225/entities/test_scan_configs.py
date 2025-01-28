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
from ...gmpv225 import GMPTestCase


class Gmpv225CloneScanConfigTestCase(GmpCloneScanConfigTestMixin, GMPTestCase):
    pass


class Gmpv225CreateScanConfigTestCase(
    GmpCreateScanConfigTestMixin, GMPTestCase
):
    pass


class Gmpv225DeleteScanConfigTestCase(
    GmpDeleteScanConfigTestMixin, GMPTestCase
):
    pass


class Gmpv225GetScanConfigTestCase(GmpGetScanConfigTestMixin, GMPTestCase):
    pass


class Gmpv225GetScanConfigsTestCase(GmpGetScanConfigsTestMixin, GMPTestCase):
    pass


class Gmpv225ImportScanConfigTestCase(
    GmpImportScanConfigTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyScanConfigSetCommentTestCase(
    GmpModifyScanConfigSetCommentTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyScanConfigSetFamilySelectionTestCase(
    GmpModifyScanConfigSetFamilySelectionTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyScanConfigSetNvtSelectionTestCase(
    GmpModifyScanConfigSetNvtSelectionTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyScanConfigSetNameTestCase(
    GmpModifyScanConfigSetNameTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyScanConfigSetNvtPreferenceTestCase(
    GmpModifyScanConfigSetNvtPreferenceTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyScanConfigSetScannerPreferenceTestCase(
    GmpModifyScanConfigSetScannerPreferenceTestMixin, GMPTestCase
):
    pass
