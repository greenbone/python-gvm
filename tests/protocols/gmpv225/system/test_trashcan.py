# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.system.trashcan import (
    GmpEmptyTrashcanTestMixin,
    GmpRestoreFromTrashcanTestMixin,
)
from ...gmpv225 import GMPTestCase


class Gmpv225EmptyTrashcanTestCase(GmpEmptyTrashcanTestMixin, GMPTestCase):
    pass


class Gmpv225RestoreFromTrashcanTestCase(
    GmpRestoreFromTrashcanTestMixin, GMPTestCase
):
    pass
