# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetResultsTestMixin:
    def test_get_results(self):
        self.gmp.get_results()

        self.connection.send.has_been_called_with(b"<get_results/>")

    def test_get_results_with_filter_string(self):
        self.gmp.get_results(filter_string="foo=bar")

        self.connection.send.has_been_called_with(
            b'<get_results filter="foo=bar"/>'
        )

    def test_get_results_with_filter_id(self):
        self.gmp.get_results(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_results filt_id="f1"/>'
        )

    def test_get_results_with_note_details(self):
        self.gmp.get_results(note_details=True)

        self.connection.send.has_been_called_with(
            b'<get_results note_details="1"/>'
        )

        self.gmp.get_results(note_details=False)

        self.connection.send.has_been_called_with(
            b'<get_results note_details="0"/>'
        )

    def test_get_results_with_override_details(self):
        self.gmp.get_results(override_details=True)

        self.connection.send.has_been_called_with(
            b'<get_results override_details="1"/>'
        )

        self.gmp.get_results(override_details=False)

        self.connection.send.has_been_called_with(
            b'<get_results override_details="0"/>'
        )

    def test_get_results_with_details(self):
        self.gmp.get_results(details=True)

        self.connection.send.has_been_called_with(b'<get_results details="1"/>')

        self.gmp.get_results(details=False)

        self.connection.send.has_been_called_with(b'<get_results details="0"/>')

    def test_get_results_with_task_id(self):
        self.gmp.get_results(task_id="t1")

        self.connection.send.has_been_called_with(
            b'<get_results task_id="t1"/>'
        )
