# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gvm.protocols.core import Request
from gvm.xml import XmlCommand


class Features:
    @classmethod
    def get_features(cls) -> Request:
        """Request a list of optional features."""
        return XmlCommand("get_features")
