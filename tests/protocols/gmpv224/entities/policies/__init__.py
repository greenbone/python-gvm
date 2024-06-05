# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_policy import GmpClonePolicyTestMixin
from .test_create_policy import GmpCreatePolicyTestMixin
from .test_delete_policy import GmpDeletePolicyTestMixin
from .test_get_policies import GmpGetPoliciesTestMixin
from .test_get_policy import GmpGetPolicyTestMixin
from .test_import_policy import GmpImportPolicyTestMixin
from .test_modify_policy_set_comment import GmpModifyPolicySetCommentTestMixin
from .test_modify_policy_set_family_selection import (
    GmpModifyPolicySetFamilySelectionTestMixin,
)
from .test_modify_policy_set_name import GmpModifyPolicySetNameTestMixin
from .test_modify_policy_set_nvt_preference import (
    GmpModifyPolicySetNvtPreferenceTestMixin,
)
from .test_modify_policy_set_nvt_selection import (
    GmpModifyPolicySetNvtSelectionTestMixin,
)
from .test_modify_policy_set_scanner_preference import (
    GmpModifyPolicySetScannerPreferenceTestMixin,
)

__all__ = (
    "GmpClonePolicyTestMixin",
    "GmpCreatePolicyTestMixin",
    "GmpDeletePolicyTestMixin",
    "GmpGetPoliciesTestMixin",
    "GmpGetPolicyTestMixin",
    "GmpImportPolicyTestMixin",
    "GmpModifyPolicySetCommentTestMixin",
    "GmpModifyPolicySetFamilySelectionTestMixin",
    "GmpModifyPolicySetNameTestMixin",
    "GmpModifyPolicySetNvtPreferenceTestMixin",
    "GmpModifyPolicySetNvtSelectionTestMixin",
    "GmpModifyPolicySetScannerPreferenceTestMixin",
)
