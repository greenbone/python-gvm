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
from ...gmpv226 import GMPTestCase


class GMPDeleteNoteTestCase(GmpDeleteNoteTestMixin, GMPTestCase):
    pass


class GMPGetNoteTestCase(GmpGetNoteTestMixin, GMPTestCase):
    pass


class GMPGetNotesTestCase(GmpGetNotesTestMixin, GMPTestCase):
    pass


class GMPCloneNoteTestCase(GmpCloneNoteTestMixin, GMPTestCase):
    pass


class GMPCreateNoteTestCase(GmpCreateNoteTestMixin, GMPTestCase):
    pass


class GMPModifyNoteTestCase(GmpModifyNoteTestMixin, GMPTestCase):
    pass
