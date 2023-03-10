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

from ...gmpv224 import Gmpv224TestCase
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


class Gmpv224CloneScanConfigTestCase(
    GmpCloneScanConfigTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224CreateScanConfigTestCase(
    GmpCreateScanConfigTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224DeleteScanConfigTestCase(
    GmpDeleteScanConfigTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetScanConfigTestCase(GmpGetScanConfigTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetScanConfigsTestCase(
    GmpGetScanConfigsTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ImportScanConfigTestCase(
    GmpImportScanConfigTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScanConfigSetCommentTestCase(
    GmpModifyScanConfigSetCommentTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScanConfigSetFamilySelectionTestCase(
    GmpModifyScanConfigSetFamilySelectionTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScanConfigSetNvtSelectionTestCase(
    GmpModifyScanConfigSetNvtSelectionTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScanConfigSetNameTestCase(
    GmpModifyScanConfigSetNameTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScanConfigSetNvtPreferenceTestCase(
    GmpModifyScanConfigSetNvtPreferenceTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScanConfigSetScannerPreferenceTestCase(
    GmpModifyScanConfigSetScannerPreferenceTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyScanConfigTestCase(
    GmpModifyScanConfigTestMixin, Gmpv224TestCase
):
    pass
