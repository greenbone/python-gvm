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
