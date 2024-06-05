# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.policies import (
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
