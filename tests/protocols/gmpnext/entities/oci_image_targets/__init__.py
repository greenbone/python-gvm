#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_oci_image_target import GmpCloneOCIImageTargetTestMixin
from .test_create_oci_image_target import GmpCreateOCIImageTargetTestMixin
from .test_delete_oci_image_target import GmpDeleteOCIImageTargetTestMixin
from .test_get_oci_image_target import GmpGetOCIImageTargetTestMixin
from .test_get_oci_image_targets import GmpGetOCIImageTargetsTestMixin
from .test_modify_oci_image_target import GmpModifyOCIImageTargetTestMixin

__all__ = (
    "GmpCloneOCIImageTargetTestMixin",
    "GmpCreateOCIImageTargetTestMixin",
    "GmpDeleteOCIImageTargetTestMixin",
    "GmpGetOCIImageTargetTestMixin",
    "GmpGetOCIImageTargetsTestMixin",
    "GmpModifyOCIImageTargetTestMixin",
)
