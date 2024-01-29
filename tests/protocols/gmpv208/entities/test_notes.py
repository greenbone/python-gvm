# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from ...gmpv208 import Gmpv208TestCase
from .notes import (
    GmpCloneNoteTestMixin,
    GmpCreateNoteTestMixin,
    GmpDeleteNoteTestMixin,
    GmpGetNotesTestMixin,
    GmpGetNoteTestMixin,
    GmpModifyNoteTestMixin,
)


class Gmpv208DeleteNoteTestCase(GmpDeleteNoteTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetNoteTestCase(GmpGetNoteTestMixin, Gmpv208TestCase):
    pass


class Gmpv208GetNotesTestCase(GmpGetNotesTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CloneNoteTestCase(GmpCloneNoteTestMixin, Gmpv208TestCase):
    pass


class Gmpv208CreateNoteTestCase(GmpCreateNoteTestMixin, Gmpv208TestCase):
    pass


class Gmpv208ModifyNoteTestCase(GmpModifyNoteTestMixin, Gmpv208TestCase):
    pass
