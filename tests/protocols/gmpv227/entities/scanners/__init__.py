# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_create_scanner import GmpCreateScannerTestMixin
from .test_modify_scanner import GmpModifyScannerTestMixin

from ....gmpv224.entities.scanners import GmpCloneScannerTestMixin
from ....gmpv224.entities.scanners import GmpDeleteScannerTestMixin
from ....gmpv224.entities.scanners import GmpGetScannerTestMixin
from ....gmpv224.entities.scanners import GmpGetScannersTestMixin
from ....gmpv224.entities.scanners import GmpVerifyScannerTestMixin

__all__ = (
    "GmpCloneScannerTestMixin",
    "GmpCreateScannerTestMixin",
    "GmpDeleteScannerTestMixin",
    "GmpGetScannerTestMixin",
    "GmpGetScannersTestMixin",
    "GmpModifyScannerTestMixin",
    "GmpVerifyScannerTestMixin",
)
