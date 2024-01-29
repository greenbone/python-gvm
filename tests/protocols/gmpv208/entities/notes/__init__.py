# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .test_clone_note import GmpCloneNoteTestMixin
from .test_create_note import GmpCreateNoteTestMixin
from .test_delete_note import GmpDeleteNoteTestMixin
from .test_get_note import GmpGetNoteTestMixin
from .test_get_notes import GmpGetNotesTestMixin
from .test_modify_note import GmpModifyNoteTestMixin

__all__ = (
    "GmpCloneNoteTestMixin",
    "GmpCreateNoteTestMixin",
    "GmpDeleteNoteTestMixin",
    "GmpGetNoteTestMixin",
    "GmpGetNotesTestMixin",
    "GmpModifyNoteTestMixin",
)
