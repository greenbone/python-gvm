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
from ...gmpv225 import GMPTestCase


class Gmpv225DeleteNoteTestCase(GmpDeleteNoteTestMixin, GMPTestCase):
    pass


class Gmpv225GetNoteTestCase(GmpGetNoteTestMixin, GMPTestCase):
    pass


class Gmpv225GetNotesTestCase(GmpGetNotesTestMixin, GMPTestCase):
    pass


class Gmpv225CloneNoteTestCase(GmpCloneNoteTestMixin, GMPTestCase):
    pass


class Gmpv225CreateNoteTestCase(GmpCreateNoteTestMixin, GMPTestCase):
    pass


class Gmpv225ModifyNoteTestCase(GmpModifyNoteTestMixin, GMPTestCase):
    pass
