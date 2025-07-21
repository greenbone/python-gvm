# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .agent_groups.test_clone_agent_group import (
    GmpCloneAgentGroupTestMixin,
)
from .agent_groups.test_create_agent_group import (
    GmpCreateAgentGroupTestMixin,
)
from .agent_groups.test_delete_agent_group import (
    GmpDeleteAgentGroupTestMixin,
)
from .agent_groups.test_get_agent_group import (
    GmpGetAgentGroupTestMixin,
)
from .agent_groups.test_get_agent_groups import (
    GmpGetAgentGroupsTestMixin,
)
from .agent_groups.test_modify_agent_group import (
    GmpModifyAgentGroupTestMixin,
)


class GMPGetAgentGroupsTestCase(GmpGetAgentGroupsTestMixin, GMPTestCase):
    pass


class GMPGetAgentGroupTestCase(GmpGetAgentGroupTestMixin, GMPTestCase):
    pass


class GMPCreateAgentGroupTestCase(GmpCreateAgentGroupTestMixin, GMPTestCase):
    pass


class GMPCloneAgentGroupTestCase(GmpCloneAgentGroupTestMixin, GMPTestCase):
    pass


class GMPModifyAgentGroupTestCase(GmpModifyAgentGroupTestMixin, GMPTestCase):
    pass


class GMPDeleteAgentGroupTestCase(GmpDeleteAgentGroupTestMixin, GMPTestCase):
    pass
