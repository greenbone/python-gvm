#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#
from tests.protocols.gmpv224.entities.scanners import GmpVerifyScannerTestMixin
from tests.protocols.gmpv227 import GMPTestCase
from tests.protocols.gmpv227.entities.scanners import (
    GmpCloneScannerTestMixin,
    GmpCreateScannerTestMixin,
    GmpDeleteScannerTestMixin,
    GmpGetScannersTestMixin,
    GmpGetScannerTestMixin,
    GmpModifyScannerTestMixin,
)


class GMPDeleteScannerTestCase(GmpDeleteScannerTestMixin, GMPTestCase):
    pass


class GMPGetScannerTestCase(GmpGetScannerTestMixin, GMPTestCase):
    pass


class GMPGetScannersTestCase(GmpGetScannersTestMixin, GMPTestCase):
    pass


class GMPCloneScannerTestCase(GmpCloneScannerTestMixin, GMPTestCase):
    pass


class GMPCreateScannerTestCase(GmpCreateScannerTestMixin, GMPTestCase):
    pass


class GMPModifyScannerTestCase(GmpModifyScannerTestMixin, GMPTestCase):
    pass


class GMPVerifyScannerTestCase(GmpVerifyScannerTestMixin, GMPTestCase):
    pass
