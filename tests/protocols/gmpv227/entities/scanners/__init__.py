# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ....gmpv224.entities.scanners import (
    GmpCloneScannerTestMixin,
    GmpDeleteScannerTestMixin,
    GmpGetScannersTestMixin,
    GmpGetScannerTestMixin,
    GmpVerifyScannerTestMixin,
)
from .test_create_scanner import GmpCreateScannerTestMixin
from .test_modify_scanner import GmpModifyScannerTestMixin

__all__ = (
    "GmpCloneScannerTestMixin",
    "GmpCreateScannerTestMixin",
    "GmpDeleteScannerTestMixin",
    "GmpGetScannerTestMixin",
    "GmpGetScannersTestMixin",
    "GmpModifyScannerTestMixin",
    "GmpVerifyScannerTestMixin",
)
