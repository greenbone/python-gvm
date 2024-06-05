# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.user_settings import (
    GmpGetUserSettingsTestMixin,
    GmpGetUserSettingTestMixin,
    GmpModifyUserSettingTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225GetUserSettingTestCase(
    GmpGetUserSettingTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225GetUserSettingsTestCase(
    GmpGetUserSettingsTestMixin, Gmpv225TestCase
):
    pass


class Gmpv225ModifyUserSettingTestCase(
    GmpModifyUserSettingTestMixin, Gmpv225TestCase
):
    pass
