# SPDX-FileCopyrightText: 2023-2025 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.operating_systems import (
    GmpDeleteOperatingSystemTestMixin,
    GmpGetOperatingSystemsTestMixin,
    GmpGetOperatingSystemTestMixin,
    GmpModifyOperatingSystemTestMixin,
)
from ...gmpv227 import GMPTestCase


class GMPDeleteOperatingSystemTestCase(
    GmpDeleteOperatingSystemTestMixin, GMPTestCase
):
    pass


class GMPGetOperatingSystemTestCase(
    GmpGetOperatingSystemTestMixin, GMPTestCase
):
    pass


class GMPGetOperatingSystemsTestCase(
    GmpGetOperatingSystemsTestMixin, GMPTestCase
):
    pass


class GMPModifyOperatingSystemTestCase(
    GmpModifyOperatingSystemTestMixin, GMPTestCase
):
    pass
