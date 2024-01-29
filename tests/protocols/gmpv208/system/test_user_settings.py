# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .user_settings import (
    GmpGetUserSettingsTestMixin,
    GmpGetUserSettingTestMixin,
    GmpModifyUserSettingTestMixin,
)


class Gmpv208GetUserSettingTestCase(
    GmpGetUserSettingTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208GetUserSettingsTestCase(
    GmpGetUserSettingsTestMixin, Gmpv208TestCase
):
    pass


class Gmpv208ModifyUserSettingTestCase(
    GmpModifyUserSettingTestMixin, Gmpv208TestCase
):
    pass
