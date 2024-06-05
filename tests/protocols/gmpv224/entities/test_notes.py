# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv224 import Gmpv224TestCase
from .notes import (
    GmpCloneNoteTestMixin,
    GmpCreateNoteTestMixin,
    GmpDeleteNoteTestMixin,
    GmpGetNotesTestMixin,
    GmpGetNoteTestMixin,
    GmpModifyNoteTestMixin,
)


class Gmpv224DeleteNoteTestCase(GmpDeleteNoteTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetNoteTestCase(GmpGetNoteTestMixin, Gmpv224TestCase):
    pass


class Gmpv224GetNotesTestCase(GmpGetNotesTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CloneNoteTestCase(GmpCloneNoteTestMixin, Gmpv224TestCase):
    pass


class Gmpv224CreateNoteTestCase(GmpCreateNoteTestMixin, Gmpv224TestCase):
    pass


class Gmpv224ModifyNoteTestCase(GmpModifyNoteTestMixin, Gmpv224TestCase):
    pass
