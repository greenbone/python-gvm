# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.trashcan import (
    GmpEmptyTrashcanTestMixin,
    GmpRestoreFromTrashcanTestMixin,
)
from ...gmpv226 import GMPTestCase


class GMPEmptyTrashcanTestCase(GmpEmptyTrashcanTestMixin, GMPTestCase):
    pass


class GMPRestoreFromTrashcanTestCase(
    GmpRestoreFromTrashcanTestMixin, GMPTestCase
):
    pass
