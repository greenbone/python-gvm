# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ...gmpv208.entities.notes import (
    GmpCloneNoteTestMixin,
    GmpDeleteNoteTestMixin,
    GmpGetNotesTestMixin,
    GmpGetNoteTestMixin,
)
from ...gmpv224 import Gmpv224TestCase
from .notes import GmpCreateNoteTestMixin, GmpModifyNoteTestMixin


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
