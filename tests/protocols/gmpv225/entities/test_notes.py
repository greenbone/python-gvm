# SPDX-FileCopyrightText: 2023-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224.entities.notes import (
    GmpCloneNoteTestMixin,
    GmpCreateNoteTestMixin,
    GmpDeleteNoteTestMixin,
    GmpGetNotesTestMixin,
    GmpGetNoteTestMixin,
    GmpModifyNoteTestMixin,
)
from ...gmpv225 import Gmpv225TestCase


class Gmpv225DeleteNoteTestCase(GmpDeleteNoteTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetNoteTestCase(GmpGetNoteTestMixin, Gmpv225TestCase):
    pass


class Gmpv225GetNotesTestCase(GmpGetNotesTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CloneNoteTestCase(GmpCloneNoteTestMixin, Gmpv225TestCase):
    pass


class Gmpv225CreateNoteTestCase(GmpCreateNoteTestMixin, Gmpv225TestCase):
    pass


class Gmpv225ModifyNoteTestCase(GmpModifyNoteTestMixin, Gmpv225TestCase):
    pass
