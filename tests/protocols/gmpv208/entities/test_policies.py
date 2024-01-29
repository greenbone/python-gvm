# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
