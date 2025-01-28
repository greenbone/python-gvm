# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.operating_systems import (
    GmpDeleteOperatingSystemTestMixin,
    GmpGetOperatingSystemsTestMixin,
    GmpGetOperatingSystemTestMixin,
    GmpModifyOperatingSystemTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteOperatingSystemTestCase(
    GmpDeleteOperatingSystemTestMixin, GMPTestCase
):
    pass


class Gmpv225GetOperatingSystemTestCase(
    GmpGetOperatingSystemTestMixin, GMPTestCase
):
    pass


class Gmpv225GetOperatingSystemsTestCase(
    GmpGetOperatingSystemsTestMixin, GMPTestCase
):
    pass


class Gmpv225ModifyOperatingSystemTestCase(
    GmpModifyOperatingSystemTestMixin, GMPTestCase
):
    pass
