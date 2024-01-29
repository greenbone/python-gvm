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
    GmpModifyScanConfigTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225CloneScanConfigTestCase(
    GmpCloneScanConfigTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225CreateScanConfigTestCase(
    GmpCreateScanConfigTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225DeleteScanConfigTestCase(
    GmpDeleteScanConfigTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetScanConfigTestCase(GmpGetScanConfigTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetScanConfigsTestCase(
    GmpGetScanConfigsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ImportScanConfigTestCase(
    GmpImportScanConfigTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScanConfigSetCommentTestCase(
    GmpModifyScanConfigSetCommentTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScanConfigSetFamilySelectionTestCase(
    GmpModifyScanConfigSetFamilySelectionTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScanConfigSetNvtSelectionTestCase(
    GmpModifyScanConfigSetNvtSelectionTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScanConfigSetNameTestCase(
    GmpModifyScanConfigSetNameTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScanConfigSetNvtPreferenceTestCase(
    GmpModifyScanConfigSetNvtPreferenceTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScanConfigSetScannerPreferenceTestCase(
    GmpModifyScanConfigSetScannerPreferenceTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyScanConfigTestCase(
    GmpModifyScanConfigTestMixin, Gmpv225TestCase
):
    pass
