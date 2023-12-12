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
from ...gmpv225 import Gmpv225TestCase


class Gmpv225ClonePolicyTestCase(GmpClonePolicyTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreatePolicyTestCase(GmpCreatePolicyTestMixin, Gmpv225TestCase):
    pass


class Gmpv225DeletePolicyTestCase(GmpDeletePolicyTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetPolicyTestCase(GmpGetPolicyTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetPoliciesTestCase(GmpGetPoliciesTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ImportPolicyTestCase(GmpImportPolicyTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestMixin, Gmpv225TestCase
):
    pass
