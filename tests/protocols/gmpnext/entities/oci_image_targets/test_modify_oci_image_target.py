#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyOCIImageTargetTestMixin:
    def test_modify_oci_image_target(self):
        self.gmp.modify_oci_image_target(oci_image_target_id="t1")

        self.connection.send.has_been_called_with(
            b'<modify_oci_image_target oci_image_target_id="t1"/>'
        )

    def test_modify_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_oci_image_target(oci_image_target_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_oci_image_target(oci_image_target_id="")

    def test_modify_target_with_comment(self):
        self.gmp.modify_oci_image_target(
            oci_image_target_id="t1", comment="foo"
        )

        self.connection.send.has_been_called_with(
            b'<modify_oci_image_target oci_image_target_id="t1">'
            b"<comment>foo</comment>"
            b"</modify_oci_image_target>"
        )

    def test_modify_target_with_image_references(self):
        self.gmp.modify_oci_image_target(
            oci_image_target_id="t1", image_references=["oci://foo/bar:latest"]
        )

        self.connection.send.has_been_called_with(
            b'<modify_oci_image_target oci_image_target_id="t1">'
            b"<image_references>oci://foo/bar:latest</image_references>"
            b"</modify_oci_image_target>"
        )

        self.gmp.modify_oci_image_target(
            oci_image_target_id="t1",
            image_references=["oci://foo/bar:latest", "oci://baz/qux:latest"],
        )

        self.connection.send.has_been_called_with(
            b'<modify_oci_image_target oci_image_target_id="t1">'
            b"<image_references>oci://foo/bar:latest,oci://baz/qux:latest</image_references>"
            b"</modify_oci_image_target>"
        )

    def test_modify_target_with_name(self):
        self.gmp.modify_oci_image_target(oci_image_target_id="t1", name="foo")

        self.connection.send.has_been_called_with(
            b'<modify_oci_image_target oci_image_target_id="t1">'
            b"<name>foo</name>"
            b"</modify_oci_image_target>"
        )

    def test_modify_target_with_smb_credential_id(self):
        self.gmp.modify_oci_image_target(
            oci_image_target_id="t1", credential_id="c1"
        )

        self.connection.send.has_been_called_with(
            b'<modify_oci_image_target oci_image_target_id="t1">'
            b'<credential id="c1"/>'
            b"</modify_oci_image_target>"
        )
