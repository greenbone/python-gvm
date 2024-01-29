# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .scanners import (
    GmpCloneScannerTestMixin,
    GmpCreateScannerTestMixin,
    GmpDeleteScannerTestMixin,
    GmpGetScannersTestMixin,
    GmpGetScannerTestMixin,
    GmpModifyScannerTestMixin,
    GmpVerifyScannerTestMixin,
)


class Gmpv208CloneScannerTestCase(GmpCloneScannerTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateScannerTestCase(GmpCreateScannerTestMixin, Gmpv208TestCase):
    pass


class Gmpv208DeleteScannerTestCase(GmpDeleteScannerTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetScannerTestCase(GmpGetScannerTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetScannersTestCase(GmpGetScannersTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyScannerTestCase(GmpModifyScannerTestMixin, Gmpv208TestCase):
    pass


class Gmpv208VerifyScannerTestMixin(GmpVerifyScannerTestMixin, Gmpv208TestCase):
    pass
