#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpCreateOCIImageTargetTestMixin:
    def test_create_target_missing_name(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_oci_image_target(
                None, image_references=["oci:foo/bar:latest"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_oci_image_target(
                name=None, image_references=["oci:foo/bar:latest"]
            )

        with self.assertRaises(RequiredArgument):
            self.gmp.create_oci_image_target(
                "", image_references=["oci:foo/bar:latest"]
            )

    def test_create_target_missing_image_references(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.create_oci_image_target(name="foo", image_references=None)

    def test_create_target_with_comment(self):
        self.gmp.create_oci_image_target(
            "foo", image_references=["oci:foo/bar:latest"], comment="bar"
        )

        self.connection.send.has_been_called_with(
            b"<create_oci_image_target>"
            b"<name>foo</name>"
            b"<image_references>oci:foo/bar:latest</image_references>"
            b"<comment>bar</comment>"
            b"</create_oci_image_target>"
        )

    def test_create_target_with_smb_credential_id(self):
        self.gmp.create_oci_image_target(
            "foo", image_references=["oci:foo/bar:latest"], credential_id="c1"
        )

        self.connection.send.has_been_called_with(
            b"<create_oci_image_target>"
            b"<name>foo</name>"
            b"<image_references>oci:foo/bar:latest</image_references>"
            b'<credential id="c1"/>'
            b"</create_oci_image_target>"
        )
