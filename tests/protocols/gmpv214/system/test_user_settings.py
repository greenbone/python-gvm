# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.user_settings import (
    GmpGetUserSettingsTestMixin,
    GmpGetUserSettingTestMixin,
    GmpModifyUserSettingTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214GetUserSettingTestCase(
    GmpGetUserSettingTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214GetUserSettingsTestCase(
    GmpGetUserSettingsTestMixin, Gmpv214TestCase
):
    pass


class Gmpv214ModifyUserSettingTestCase(
    GmpModifyUserSettingTestMixin, Gmpv214TestCase
):
    pass
