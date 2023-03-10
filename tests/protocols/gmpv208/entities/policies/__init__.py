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
