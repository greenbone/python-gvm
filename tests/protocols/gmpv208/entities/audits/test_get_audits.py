# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


class GmpGetAuditsTestMixin:
    def test_get_audits_simple(self):
        self.gmp.get_audits()

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="audit"/>'
        )

    def test_get_audits_with_filter_string(self):
        self.gmp.get_audits(filter_string="name=foo")

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="audit" filter="name=foo"/>'
        )

    def test_get_audits_with_filter_id(self):
        self.gmp.get_audits(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="audit" filt_id="f1"/>'
        )

    def test_get_audits_from_trash(self):
        self.gmp.get_audits(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="audit" trash="1"/>'
        )

    def test_get_audits_with_details(self):
        self.gmp.get_audits(details=True)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="audit" details="1"/>'
        )

    def test_get_audits_without_details(self):
        self.gmp.get_audits(details=False)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="audit" details="0"/>'
        )

    def test_get_audits_with_schedules_only(self):
        self.gmp.get_audits(schedules_only=True)

        self.connection.send.has_been_called_with(
            b'<get_tasks usage_type="audit" schedules_only="1"/>'
        )
