#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from tests.protocols.gmpv227.entities.scanners import (
    GmpCloneScannerTestMixin,
    GmpCreateScannerTestMixin,
    GmpDeleteScannerTestMixin,
    GmpGetScannersTestMixin,
    GmpGetScannerTestMixin,
    GmpModifyScannerTestMixin,
)
from tests.protocols.gmpv227 import GMPTestCase


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