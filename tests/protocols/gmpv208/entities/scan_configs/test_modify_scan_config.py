# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
import warnings

from gvm.errors import InvalidArgument, RequiredArgument


class GmpModifyScanConfigTestMixin:
    def test_modify_scan_config_invalid_selection(self):
        with self.assertRaises(InvalidArgument):
            self.gmp.modify_scan_config(config_id="c1", selection="foo")

        with self.assertRaises(InvalidArgument):
            self.gmp.modify_scan_config(config_id="c1", selection="")

    def test_modify_scan_config_missing_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config(config_id=None, selection="nvt_pref")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config(config_id="", selection="nvt_pref")

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_scan_config("", selection="nvt_pref")

    def test_modify_scan_config_set_comment(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_scan_config(
                config_id="c1", selection=None, comment="foo"
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<comment>foo</comment>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_nvt_pref(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_scan_config(
                config_id="c1", selection="nvt_pref", nvt_oid="o1", name="foo"
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b'<nvt oid="o1"/>'
            b"<name>foo</name>"
            b"</preference>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_scanner_pref(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_scan_config(
                config_id="c1", selection="scan_pref", name="foo", value="bar"
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<preference>"
            b"<name>foo</name>"
            b"<value>YmFy</value>"
            b"</preference>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_nvt_selection(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_scan_config(
                config_id="c1",
                selection="nvt_selection",
                nvt_oids=["o1"],
                family="foo",
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<nvt_selection>"
            b"<family>foo</family>"
            b'<nvt oid="o1"/>'
            b"</nvt_selection>"
            b"</modify_config>"
        )

    def test_modify_scan_config_set_family_selection(self):
        # pylint: disable=invalid-name
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.gmp.modify_scan_config(
                config_id="c1",
                selection="family_selection",
                families=[("foo", True, True)],
            )

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))

        self.connection.send.has_been_called_with(
            b'<modify_config config_id="c1">'
            b"<family_selection>"
            b"<growing>1</growing>"
            b"<family>"
            b"<name>foo</name>"
            b"<all>1</all>"
            b"<growing>1</growing>"
            b"</family>"
            b"</family_selection>"
            b"</modify_config>"
        )
