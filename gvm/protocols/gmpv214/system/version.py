# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gvm.protocols.gmpv208.system.version import (
    VersionMixin as Gmp208VersionMixin,
)

PROTOCOL_VERSION = (21, 4)


class VersionMixin(Gmp208VersionMixin):
    @staticmethod
    def get_protocol_version() -> tuple:
        """Determine the Greenbone Management Protocol (gmp) version used
        by python-gvm version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
        return PROTOCOL_VERSION
