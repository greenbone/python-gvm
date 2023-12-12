# -*- coding: utf-8 -*-
# Copyright (C) 2023 Greenbone AG
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
