#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .web_application_targets import (
    GmpCloneWebApplicationTargetTestMixin,
    GmpCreateWebApplicationTargetTestMixin,
    GmpDeleteWebApplicationTargetTestMixin,
    GmpGetWebApplicationTargetsTestMixin,
    GmpGetWebApplicationTargetTestMixin,
    GmpModifyWebApplicationTargetTestMixin,
)


class GmpCloneWebApplicationTargetTestCase(
    GmpCloneWebApplicationTargetTestMixin, GMPTestCase
):
    pass


class GmpCreateWebApplicationTargetTestCase(
    GmpCreateWebApplicationTargetTestMixin, GMPTestCase
):
    pass


class GmpDeleteWebApplicationTargetTestCase(
    GmpDeleteWebApplicationTargetTestMixin, GMPTestCase
):
    pass


class GmpGetWebApplicationTargetTestCase(
    GmpGetWebApplicationTargetTestMixin, GMPTestCase
):
    pass


class GmpGetWebApplicationTargetsTestCase(
    GmpGetWebApplicationTargetsTestMixin, GMPTestCase
):
    pass


class GmpModifyWebApplicationTargetTestCase(
    GmpModifyWebApplicationTargetTestMixin, GMPTestCase
):
    pass
