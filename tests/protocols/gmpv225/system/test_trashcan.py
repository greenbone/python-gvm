# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.system.trashcan import (
    GmpEmptyTrashcanTestMixin,
    GmpRestoreFromTrashcanTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225EmptyTrashcanTestCase(GmpEmptyTrashcanTestMixin, Gmpv225TestCase):
    pass


class Gmpv225RestoreFromTrashcanTestCase(
    GmpRestoreFromTrashcanTestMixin, Gmpv225TestCase
):
    pass
