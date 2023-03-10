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

from ...gmpv208 import Gmpv208TestCase
from .policies import (
    GmpClonePolicyTestMixin,
    GmpCreatePolicyTestMixin,
    GmpDeletePolicyTestMixin,
    GmpGetPoliciesTestMixin,
    GmpGetPolicyTestMixin,
    GmpImportPolicyTestMixin,
    GmpModifyPolicySetCommentTestMixin,
    GmpModifyPolicySetFamilySelectionTestMixin,
    GmpModifyPolicySetNameTestMixin,
    GmpModifyPolicySetNvtPreferenceTestMixin,
    GmpModifyPolicySetNvtSelectionTestMixin,
    GmpModifyPolicySetScannerPreferenceTestMixin,
)


class Gmpv208ClonePolicyTestCase(GmpClonePolicyTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreatePolicyTestCase(GmpCreatePolicyTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DeletePolicyTestCase(GmpDeletePolicyTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetPolicyTestCase(GmpGetPolicyTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetPoliciesTestCase(GmpGetPoliciesTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ImportPolicyTestCase(GmpImportPolicyTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestMixin, Gmpv208TestCase
):
    pass
