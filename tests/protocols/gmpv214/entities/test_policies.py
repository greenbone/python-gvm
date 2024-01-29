# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
