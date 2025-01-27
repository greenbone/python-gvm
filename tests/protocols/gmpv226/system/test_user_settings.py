# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.user_settings import (
    GmpGetUserSettingsTestMixin,
    GmpGetUserSettingTestMixin,
    GmpModifyUserSettingTestMixin,
)
from ...gmpv226 import GMPTestCase


class GMPGetUserSettingTestCase(GmpGetUserSettingTestMixin, GMPTestCase):
    pass


class GMPGetUserSettingsTestCase(GmpGetUserSettingsTestMixin, GMPTestCase):
    pass


class GMPModifyUserSettingTestCase(GmpModifyUserSettingTestMixin, GMPTestCase):
    pass
