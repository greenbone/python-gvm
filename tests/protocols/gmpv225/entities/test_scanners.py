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
    GmpVerifyScannerTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteScannerTestCase(GmpDeleteScannerTestMixin, GMPTestCase):
    pass


class Gmpv225GetScannerTestCase(GmpGetScannerTestMixin, GMPTestCase):
    pass


class Gmpv225GetScannersTestCase(GmpGetScannersTestMixin, GMPTestCase):
    pass


class Gmpv225CloneScannerTestCase(GmpCloneScannerTestMixin, GMPTestCase):
    pass


class Gmpv225CreateScannerTestCase(GmpCreateScannerTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyScannerTestCase(GmpModifyScannerTestMixin, GMPTestCase):
    pass


class Gmpv225VerifyScannerTestCase(GmpVerifyScannerTestMixin, GMPTestCase):
    pass
