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
from ...gmpv226 import GMPTestCase


class GMPClonePolicyTestCase(GmpClonePolicyTestMixin, GMPTestCase):
    pass


class GMPCreatePolicyTestCase(GmpCreatePolicyTestMixin, GMPTestCase):
    pass


class GMPDeletePolicyTestCase(GmpDeletePolicyTestMixin, GMPTestCase):
    pass


class GMPGetPolicyTestCase(GmpGetPolicyTestMixin, GMPTestCase):
    pass


class GMPGetPoliciesTestCase(GmpGetPoliciesTestMixin, GMPTestCase):
    pass


class GMPImportPolicyTestCase(GmpImportPolicyTestMixin, GMPTestCase):
    pass


class GMPModifyPolicySetCommentTestCase(
    GmpModifyPolicySetCommentTestMixin, GMPTestCase
):
    pass


class GMPModifyPolicySetFamilySelectionTestCase(
    GmpModifyPolicySetFamilySelectionTestMixin, GMPTestCase
):
    pass


class GMPModifyPolicySetNvtSelectionTestCase(
    GmpModifyPolicySetNvtSelectionTestMixin, GMPTestCase
):
    pass


class GMPModifyPolicySetNameTestCase(
    GmpModifyPolicySetNameTestMixin, GMPTestCase
):
    pass


class GMPModifyPolicySetNvtPreferenceTestCase(
    GmpModifyPolicySetNvtPreferenceTestMixin, GMPTestCase
):
    pass


class GMPModifyPolicySetScannerPreferenceTestCase(
    GmpModifyPolicySetScannerPreferenceTestMixin, GMPTestCase
):
    pass
