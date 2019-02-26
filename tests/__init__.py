# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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


class CallableMock:
    def __init__(self, name):
        self.name = name
        self.calls = []
        self.result = None

    def __call__(self, *args, **kwargs):
        self.calls.append({'args': args, 'kwargs': kwargs})

        return self.result

    def return_value(self, value):
        self.result = value

    def has_not_been_called(self):
        assert len(self.calls) == 0, "{0} has been called.".format(self.name)

    def has_been_called(self):
        assert len(self.calls) > 0, "{0} has not been called.".format(self.name)

    def has_been_called_times(self, times):
        assert len(self.calls) == times, (
            "{name} has not been called {times}"
            " times.".format(name=self.name, times=times)
        )

    def has_been_called_with(self, *args, **kwargs):
        if len(self.calls) == 0:
            assert False

        lastcall = self.calls[-1]

        # not sure if this is correct
        assert lastcall['args'] == args and lastcall['kwargs'] == kwargs, (
            "Expected arguments {eargs} {ekwargs} of {name} do not match."
            "Received: {rargs} {rkwargs}".format(
                name=self.name,
                eargs=args,
                ekwargs=kwargs,
                rargs=lastcall['args'],
                rkwargs=lastcall['kwargs'],
            )
        )
