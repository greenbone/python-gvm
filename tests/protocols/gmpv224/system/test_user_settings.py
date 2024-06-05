# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .user_settings import (
    GmpGetUserSettingsTestMixin,
    GmpGetUserSettingTestMixin,
    GmpModifyUserSettingTestMixin,
)


class Gmpv224GetUserSettingTestCase(
    GmpGetUserSettingTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224GetUserSettingsTestCase(
    GmpGetUserSettingsTestMixin, Gmpv224TestCase
):
    pass


class Gmpv224ModifyUserSettingTestCase(
    GmpModifyUserSettingTestMixin, Gmpv224TestCase
):
    pass
