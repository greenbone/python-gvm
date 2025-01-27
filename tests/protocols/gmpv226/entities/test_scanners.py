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
from ...gmpv226 import GMPTestCase


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
