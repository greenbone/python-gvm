# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
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

from ...gmpv2110 import Gmpv2110TestCase
from ...gmpv208.entities.scan_configs import (
    GmpCloneScanConfigTestMixin,
    GmpCreateScanConfigTestMixin,
    GmpCreateScanConfigFromOSPScannerTestMixin,
    GmpDeleteScanConfigTestMixin,
    GmpGetScanConfigTestMixin,
    GmpGetScanConfigsTestMixin,
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


class Gmpv2110CloneScanConfigTestCase(
    GmpCloneScanConfigTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110CreateScanConfigTestCase(
    GmpCreateScanConfigTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110CreateScanConfigFromOSPScannerTestCase(
    GmpCreateScanConfigFromOSPScannerTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110DeleteScanConfigTestCase(
    GmpDeleteScanConfigTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110GetScanConfigTestCase(
    GmpGetScanConfigTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110GetScanConfigsTestCase(
    GmpGetScanConfigsTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ImportScanConfigTestCase(
    GmpImportScanConfigTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ModifyScanConfigSetCommentTestCase(
    GmpModifyScanConfigSetCommentTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ModifyScanConfigSetFamilySelectionTestCase(
    GmpModifyScanConfigSetFamilySelectionTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ModifyScanConfigSetNvtSelectionTestCase(
    GmpModifyScanConfigSetNvtSelectionTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ModifyScanConfigSetNameTestCase(
    GmpModifyScanConfigSetNameTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ModifyScanConfigSetNvtPreferenceTestCase(
    GmpModifyScanConfigSetNvtPreferenceTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ModifyScanConfigSetScannerPreferenceTestCase(
    GmpModifyScanConfigSetScannerPreferenceTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110ModifyScanConfigTestCase(
    GmpModifyScanConfigTestMixin, Gmpv2110TestCase
):
    pass


class Gmpv2110SyncScanConfigTestCase(
    GmpSyncScanConfigTestMixin, Gmpv2110TestCase
):
    pass
