# SPDX-FileCopyrightText: 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from ...gmpnext import GMPTestCase
from .features.test_get_features import (
    GmpGetFeaturesTestMixin,
)


class GmpGetFeaturesTestCase(GmpGetFeaturesTestMixin, GMPTestCase):
    pass
