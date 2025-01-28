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
from ...gmpv225 import GMPTestCase


class Gmpv225ClonePolicyTestCase(GmpClonePolicyTestMixin, GMPTestCase):
    pass


class Gmpv225CreatePolicyTestCase(GmpCreatePolicyTestMixin, GMPTestCase):
    pass


class Gmpv225DeletePolicyTestCase(GmpDeletePolicyTestMixin, GMPTestCase):
    pass


class Gmpv225GetPolicyTestCase(GmpGetPolicyTestMixin, GMPTestCase):
    pass


class Gmpv225GetPoliciesTestCase(GmpGetPoliciesTestMixin, GMPTestCase):
    pass


class Gmpv225ImportPolicyTestCase(GmpImportPolicyTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestMixin, GMPTestCase
):
    pass
