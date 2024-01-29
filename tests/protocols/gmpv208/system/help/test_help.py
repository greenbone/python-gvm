# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import InvalidArgumentType
from gvm.protocols.gmpv208 import HelpFormat


class GmpHelpTestMixin:
    def test_help(self):
        self.gmp.help()

        self.connection.send.has_been_called_with('<help type=""/>')

    def test_help_type_brief(self):
        self.gmp.help(brief=True)

        self.connection.send.has_been_called_with('<help type="brief"/>')

    def test_invalid_help_format(self):
        with self.assertRaises(InvalidArgumentType):
            self.gmp.help(help_format="foo")

    def test_html_format(self):
        self.gmp.help(help_format=HelpFormat.HTML)

        self.connection.send.has_been_called_with(
            '<help type="" format="html"/>'
        )
