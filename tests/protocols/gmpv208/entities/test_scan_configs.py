# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .scan_configs import (
    GmpCloneScanConfigTestMixin,
    GmpCreateScanConfigFromOSPScannerTestMixin,
    GmpCreateScanConfigTestMixin,
    GmpDeleteScanConfigTestMixin,
    GmpGetScanConfigPreferencesTestMixin,
    GmpGetScanConfigPreferenceTestMixin,
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


class Gmpv208CloneScanConfigTestCase(
    GmpCloneScanConfigTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CreateScanConfigTestCase(
    GmpCreateScanConfigTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208CreateScanConfigFromOSPScannerTestCase(
    GmpCreateScanConfigFromOSPScannerTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208DeleteScanConfigTestCase(
    GmpDeleteScanConfigTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetScanConfigTestCase(GmpGetScanConfigTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetScanConfigsTestCase(
    GmpGetScanConfigsTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetScanConfigPreferenceTestCase(
    GmpGetScanConfigPreferenceTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetScanConfigPreferencesTestCase(
    GmpGetScanConfigPreferencesTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ImportScanConfigTestCase(
    GmpImportScanConfigTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScanConfigSetCommentTestCase(
    GmpModifyScanConfigSetCommentTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScanConfigSetFamilySelectionTestCase(
    GmpModifyScanConfigSetFamilySelectionTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScanConfigSetNvtSelectionTestCase(
    GmpModifyScanConfigSetNvtSelectionTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScanConfigSetNameTestCase(
    GmpModifyScanConfigSetNameTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScanConfigSetNvtPreferenceTestCase(
    GmpModifyScanConfigSetNvtPreferenceTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScanConfigSetScannerPreferenceTestCase(
    GmpModifyScanConfigSetScannerPreferenceTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyScanConfigTestCase(
    GmpModifyScanConfigTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208SyncScanConfigTestCase(
    GmpSyncScanConfigTestMixin, Gmpv208TestCase
):
    pass
