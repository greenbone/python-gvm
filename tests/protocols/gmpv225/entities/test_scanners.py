# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.scanners import (
    GmpCloneScannerTestMixin,
    GmpCreateScannerTestMixin,
    GmpDeleteScannerTestMixin,
    GmpGetScannersTestMixin,
    GmpGetScannerTestMixin,
    GmpModifyScannerTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteScannerTestCase(GmpDeleteScannerTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetScannerTestCase(GmpGetScannerTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetScannersTestCase(GmpGetScannersTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneScannerTestCase(GmpCloneScannerTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateScannerTestCase(GmpCreateScannerTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyScannerTestCase(GmpModifyScannerTestMixin, Gmpv225TestCase):
    pass
