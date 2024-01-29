# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.scanners import (
    GmpCloneScannerTestMixin,
    GmpDeleteScannerTestMixin,
    GmpGetScannersTestMixin,
    GmpGetScannerTestMixin,
)
from ...gmpv214 import Gmpv214TestCase
from .scanners import GmpCreateScannerTestMixin, GmpModifyScannerTestMixin


class Gmpv214DeleteScannerTestCase(GmpDeleteScannerTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetScannerTestCase(GmpGetScannerTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetScannersTestCase(GmpGetScannersTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneScannerTestCase(GmpCloneScannerTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateScannerTestCase(GmpCreateScannerTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyScannerTestCase(GmpModifyScannerTestMixin, Gmpv214TestCase):
    pass
