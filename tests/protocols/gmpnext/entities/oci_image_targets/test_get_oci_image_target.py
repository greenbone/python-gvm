#  SPDX-FileCopyrightText: 2025 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpGetOCIImageTargetTestMixin:
    def test_get_target(self):
        self.gmp.get_oci_image_target("t1")

        self.connection.send.has_been_called_with(
            b'<get_oci_image_targets oci_image_target_id="t1"/>'
        )

        self.gmp.get_oci_image_target(oci_image_target_id="t1")

        self.connection.send.has_been_called_with(
            b'<get_oci_image_targets oci_image_target_id="t1"/>'
        )

    def test_get_target_missing_target_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.get_oci_image_target(oci_image_target_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.get_oci_image_target("")

    def test_get_target_with_tasks(self):
        self.gmp.get_oci_image_target(oci_image_target_id="t1", tasks=True)

        self.connection.send.has_been_called_with(
            b'<get_oci_image_targets oci_image_target_id="t1" tasks="1"/>'
        )

        self.gmp.get_oci_image_target(oci_image_target_id="t1", tasks=False)

        self.connection.send.has_been_called_with(
            b'<get_oci_image_targets oci_image_target_id="t1" tasks="0"/>'
        )
