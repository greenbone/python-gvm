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
from ...gmpv224 import Gmpv224TestCase


class Gmpv224ClonePolicyTestCase(GmpClonePolicyTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreatePolicyTestCase(GmpCreatePolicyTestMixin, Gmpv224TestCase):
    pass


class Gmpv224DeletePolicyTestCase(GmpDeletePolicyTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetPolicyTestCase(GmpGetPolicyTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetPoliciesTestCase(GmpGetPoliciesTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ImportPolicyTestCase(GmpImportPolicyTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestMixin, Gmpv224TestCase
):
    pass
