# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.trashcan import (
    GmpEmptyTrashcanTestMixin,
    GmpRestoreFromTrashcanTestMixin,
)
from ...gmpv214 import Gmpv214TestCase


class Gmpv214EmptyTrashcanTestCase(GmpEmptyTrashcanTestMixin, Gmpv214TestCase):
    pass


class Gmpv214RestoreFromTrashcanTestCase(
    GmpRestoreFromTrashcanTestMixin, Gmpv214TestCase
):
    pass
