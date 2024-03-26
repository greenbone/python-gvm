# SPDX-FileCopyrightText: 2021-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm._enum import Enum


class ReportFormatType(Enum):
    """Enum for builtin report formats"""

    ANONYMOUS_XML = "5057e5cc-b825-11e4-9d0e-28d24461215b"
    ARF = "910200ca-dc05-11e1-954f-406186ea4fc5"
    CPE = "5ceff8ba-1f62-11e1-ab9f-406186ea4fc5"
    CSV_HOSTS = '9087b18c-626c-11e3-8892-406186ea4fc5"'
    CSV_RESULTS = "c1645568-627a-11e3-a660-406186ea4fc5"
    GCR_PDF = "dc51a40a-c022-11e9-b02d-3f7ca5bdcb11"
    GSR_HTML = "ffa123c9-a2d2-409e-bbbb-a6c1385dbeaa"
    GSR_PDF = "35ba7077-dc85-42ef-87c9-b0eda7e903b6"
    GXCR_PDF = "f0d348de-c022-11e9-bc4c-4bf1d5e1a8ca"
    GXR_PDF = "ebbc7f34-8ae5-11e1-b07b-001f29eadec8"
    ITG = "77bd6c4a-1f62-11e1-abf0-406186ea4fc5"
    LATEX = "a684c02c-b531-11e1-bdc2-406186ea4fc5"
    NBE = "9ca6fe72-1f62-11e1-9e7c-406186ea4fc5"
    PDF = "c402cc3e-b531-11e1-9163-406186ea4fc5"
    SVG = "9e5e5deb-879e-4ecc-8be6-a71cd0875cdd"
    TXT = "a3810a62-1f62-11e1-9219-406186ea4fc5"
    VERINICE_ISM = "c15ad349-bd8d-457a-880a-c7056532ee15"
    VERINICE_ITG = "50c9950a-f326-11e4-800c-28d24461215b"
    XML = "a994b278-1f62-11e1-96ac-406186ea4fc5"

    def __str__(self) -> str:
        return self.value
