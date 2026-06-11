# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from ...gmpnext.entities.targets import (
    GmpCloneTargetTestMixin,
    GmpCreateTargetTestMixin,
    GmpDeleteTargetTestMixin,
    GmpGetTargetsTestMixin,
    GmpGetTargetTestMixin,
    GmpModifyTargetTestMixin,
)


class GMPCloneTargetTestCase(GmpCloneTargetTestMixin, GMPTestCase):
    pass


class GMPCreateTargetTestCase(GmpCreateTargetTestMixin, GMPTestCase):
    pass


class GMPDeleteTargetTestCase(GmpDeleteTargetTestMixin, GMPTestCase):
    pass


class GMPGetTargetTestCase(GmpGetTargetTestMixin, GMPTestCase):
    pass


class GMPGetTargetsTestCase(GmpGetTargetsTestMixin, GMPTestCase):
    pass


class GMPModifyTargetTestCase(GmpModifyTargetTestMixin, GMPTestCase):
    pass
