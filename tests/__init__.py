# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class CallableMock:
    def __init__(self, name):
        self.name = name
        self.calls = []
        self.result = None

    def __call__(self, *args, **kwargs):
        self.calls.append({"args": args, "kwargs": kwargs})

        return self.result

    def return_value(self, value):
        self.result = value

    def has_not_been_called(self):
        assert len(self.calls) == 0, f"{self.name} has been called."

    def has_been_called(self):
        assert len(self.calls) > 0, f"{self.name} has not been called."

    def has_been_called_times(self, times):
        assert (
            len(self.calls) == times
        ), f"{self.name} has not been called {times} times."

    def has_been_called_with(self, *args, **kwargs):
        if len(self.calls) == 0:
            assert False

        lastcall = self.calls[-1]

        resp = (
            "Expected arguments {eargs} {ekwargs} of {name} do not match. "
            "Received: {rargs} {rkwargs}"
        )

        # not sure if this is correct
        assert (
            lastcall["args"] == args and lastcall["kwargs"] == kwargs
        ), resp.format(
            name=self.name,
            eargs=args,
            ekwargs=kwargs,
            rargs=lastcall["args"],
            rkwargs=lastcall["kwargs"],
        )
