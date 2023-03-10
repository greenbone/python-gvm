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

from ...gmpv208.entities.policies import (
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
from ...gmpv214 import Gmpv214TestCase


class Gmpv214ClonePolicyTestCase(GmpClonePolicyTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreatePolicyTestCase(GmpCreatePolicyTestMixin, Gmpv214TestCase):
    pass


class Gmpv214DeletePolicyTestCase(GmpDeletePolicyTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetPolicyTestCase(GmpGetPolicyTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetPoliciesTestCase(GmpGetPoliciesTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ImportPolicyTestCase(GmpImportPolicyTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestMixin, Gmpv214TestCase
):
    pass
