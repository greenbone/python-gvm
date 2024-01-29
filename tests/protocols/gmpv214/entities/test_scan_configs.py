# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.scan_configs import (
    GmpCloneScanConfigTestMixin,
    GmpCreateScanConfigFromOSPScannerTestMixin,
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
    GmpModifyScanConfigTestMixin,
    GmpSyncScanConfigTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214CloneScanConfigTestCase(
    GmpCloneScanConfigTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreateScanConfigTestCase(
    GmpCreateScanConfigTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214CreateScanConfigFromOSPScannerTestCase(
    GmpCreateScanConfigFromOSPScannerTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214DeleteScanConfigTestCase(
    GmpDeleteScanConfigTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetScanConfigTestCase(GmpGetScanConfigTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetScanConfigsTestCase(
    GmpGetScanConfigsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ImportScanConfigTestCase(
    GmpImportScanConfigTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScanConfigSetCommentTestCase(
    GmpModifyScanConfigSetCommentTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScanConfigSetFamilySelectionTestCase(
    GmpModifyScanConfigSetFamilySelectionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScanConfigSetNvtSelectionTestCase(
    GmpModifyScanConfigSetNvtSelectionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScanConfigSetNameTestCase(
    GmpModifyScanConfigSetNameTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScanConfigSetNvtPreferenceTestCase(
    GmpModifyScanConfigSetNvtPreferenceTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScanConfigSetScannerPreferenceTestCase(
    GmpModifyScanConfigSetScannerPreferenceTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyScanConfigTestCase(
    GmpModifyScanConfigTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214SyncScanConfigTestCase(
    GmpSyncScanConfigTestMixin, Gmpv214TestCase
):
    pass
