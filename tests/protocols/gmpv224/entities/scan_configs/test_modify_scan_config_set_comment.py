# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyScanConfigSetCommentTestMixin:
    def test_modify_scan_config_set_comment(self):
        self.gmp.modify_scan_config_set_comment("c1")

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<comment></comment>"
            b"</modify_config>"
        )

        self.gmp.modify_scan_config_set_comment("c1", comment="foo")

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<comment>foo</comment>"
            b"</modify_config>"
        )

        self.gmp.modify_scan_config_set_comment("c1", comment=None)

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<comment></comment>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_comment_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_comment(config_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_comment("")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config_set_comment(config_id="")
