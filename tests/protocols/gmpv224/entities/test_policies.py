# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
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
