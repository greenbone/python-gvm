# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208.entities.notes import (
    GmpCloneNoteTestMixin,
    GmpDeleteNoteTestMixin,
    GmpGetNotesTestMixin,
    GmpGetNoteTestMixin,
)
from ...gmpv214 import Gmpv214TestCase
from .notes import GmpCreateNoteTestMixin, GmpModifyNoteTestMixin


class Gmpv214DeleteNoteTestCase(GmpDeleteNoteTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetNoteTestCase(GmpGetNoteTestMixin, Gmpv214TestCase):
    pass


class Gmpv214GetNotesTestCase(GmpGetNotesTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CloneNoteTestCase(GmpCloneNoteTestMixin, Gmpv214TestCase):
    pass


class Gmpv214CreateNoteTestCase(GmpCreateNoteTestMixin, Gmpv214TestCase):
    pass


class Gmpv214ModifyNoteTestCase(GmpModifyNoteTestMixin, Gmpv214TestCase):
    pass
