# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.trashcan import (
    GmpEmptyTrashcanTestMixin,
    GmpRestoreFromTrashcanTestMixin,
)
from ...gmpv224 import Gmpv224TestCase


class Gmpv224EmptyTrashcanTestCase(GmpEmptyTrashcanTestMixin, Gmpv224TestCase):
    pass


class Gmpv224RestoreFromTrashcanTestCase(
    GmpRestoreFromTrashcanTestMixin, Gmpv224TestCase
):
    pass
