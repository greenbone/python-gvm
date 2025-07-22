#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpnext import GMPTestCase
from .oci_image_targets import (
    GmpCloneOCIImageTargetTestMixin,
    GmpCreateOCIImageTargetTestMixin,
    GmpDeleteOCIImageTargetTestMixin,
    GmpGetOCIImageTargetsTestMixin,
    GmpGetOCIImageTargetTestMixin,
    GmpModifyOCIImageTargetTestMixin,
)


class GmpCloneOCIImageTargetTestCase(
    GmpCloneOCIImageTargetTestMixin, GMPTestCase
):
    pass


class GmpCreateOCIImageTargetTestCase(
    GmpCreateOCIImageTargetTestMixin, GMPTestCase
):
    pass


class GmpDeleteOCIImageTargetTestCase(
    GmpDeleteOCIImageTargetTestMixin, GMPTestCase
):
    pass


class GmpGetOCIImageTargetTestCase(GmpGetOCIImageTargetsTestMixin, GMPTestCase):
    pass


class GmpGetOCIImageTargetsTestCase(GmpGetOCIImageTargetTestMixin, GMPTestCase):
    pass


class GmpModifyOCIImageTargetTestCase(
    GmpModifyOCIImageTargetTestMixin, GMPTestCase
):
    pass
