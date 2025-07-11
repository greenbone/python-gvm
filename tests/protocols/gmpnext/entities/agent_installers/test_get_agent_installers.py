#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later


class GmpGetAgentInstallersTestMixin:
    def test_get_agent_installers(self):
        self.gmp.get_agent_installers()

        self.connection.send.has_been_called_with(b"<get_agent_installers/>")

    def test_get_agent_installers_trash(self):
        self.gmp.get_agent_installers(trash=True)

        self.connection.send.has_been_called_with(
            b'<get_agent_installers trash="1"/>'
        )

    def test_get_agent_installers_with_filter_string(self):
        self.gmp.get_agent_installers(
            filter_string="name=foo",
        )

        self.connection.send.has_been_called_with(
            b'<get_agent_installers filter="name=foo"/>'
        )

    def test_get_agent_installers_with_filter_id(self):
        self.gmp.get_agent_installers(filter_id="f1")

        self.connection.send.has_been_called_with(
            b'<get_agent_installers filt_id="f1"/>'
        )

    def test_get_agent_installers_with_details(self):
        self.gmp.get_agent_installers(details=True)

        self.connection.send.has_been_called_with(
            b'<get_agent_installers details="1"/>'
        )

    def test_get_agent_installers_without_details(self):
        self.gmp.get_agent_installers(details=False)

        self.connection.send.has_been_called_with(
            b'<get_agent_installers details="0"/>'
        )
