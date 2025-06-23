# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Main module of python-gvm.
"""

from .__version__ import __version__


def get_version() -> str:
    """Returns the version of python-gvm as a string in
    `PEP440 <https://www.python.org/dev/peps/pep-0440>`_ compliant format.

    Returns:
        Current version of python-gvm
    """
    return __version__
