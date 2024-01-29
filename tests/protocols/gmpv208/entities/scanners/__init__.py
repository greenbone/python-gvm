# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_scanner import GmpCloneScannerTestMixin
from .test_create_scanner import GmpCreateScannerTestMixin
from .test_delete_scanner import GmpDeleteScannerTestMixin
from .test_get_scanner import GmpGetScannerTestMixin
from .test_get_scanners import GmpGetScannersTestMixin
from .test_modify_scanner import GmpModifyScannerTestMixin
from .test_verify_scanner import GmpVerifyScannerTestMixin

__all__ = (
    "GmpCloneScannerTestMixin",
    "GmpCreateScannerTestMixin",
    "GmpDeleteScannerTestMixin",
    "GmpGetScannerTestMixin",
    "GmpGetScannersTestMixin",
    "GmpModifyScannerTestMixin",
    "GmpVerifyScannerTestMixin",
)
