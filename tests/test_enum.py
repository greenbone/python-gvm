# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from gvm._enum import Enum
from gvm.errors import InvalidArgument


class SomeEnum(Enum):
    FOO = "foo"
    BAR = "bar"
    LOREM = "ipsum"


class OtherEnum(Enum):
    LOREM = "ipsum"


class SomeClass:
    def __str__(self) -> str:
        return "foo"


class EnumTestCase(unittest.TestCase):
    def test_enum(self) -> None:
        enum = SomeEnum("FOO")
        self.assertEqual(enum, SomeEnum.FOO)
        enum = SomeEnum("BAR")
        self.assertEqual(enum, SomeEnum.BAR)

        enum = SomeEnum("foo")
        self.assertEqual(enum, SomeEnum.FOO)
        enum = SomeEnum("bar")
        self.assertEqual(enum, SomeEnum.BAR)

        enum = SomeEnum(SomeClass())
        self.assertEqual(enum, SomeEnum.FOO)

        enum = SomeEnum(SomeEnum.BAR)
        self.assertEqual(enum, SomeEnum.BAR)

        enum = SomeEnum(SomeEnum.LOREM)
        self.assertEqual(enum, SomeEnum.LOREM)

        enum = SomeEnum("ipsum")
        self.assertEqual(enum, SomeEnum.LOREM)

        enum = SomeEnum(OtherEnum.LOREM)
        self.assertEqual(enum, SomeEnum.LOREM)

    def test_invalid(self) -> None:
        with self.assertRaisesRegex(
            InvalidArgument,
            "^Invalid argument BAZ. Allowed values are FOO,BAR,LOREM.$",
        ):
            SomeEnum("BAZ")

        with self.assertRaisesRegex(
            ValueError,
            "^'' is not a valid SomeEnum$",
        ):
            SomeEnum("")

        with self.assertRaisesRegex(
            ValueError,
            "^None is not a valid SomeEnum$",
        ):
            SomeEnum(None)

    def test_from_string(self) -> None:
        enum = SomeEnum.from_string("FOO")
        self.assertEqual(enum, SomeEnum.FOO)
        enum = SomeEnum.from_string("BAR")
        self.assertEqual(enum, SomeEnum.BAR)

        enum = SomeEnum.from_string("foo")
        self.assertEqual(enum, SomeEnum.FOO)
        enum = SomeEnum.from_string("bar")
        self.assertEqual(enum, SomeEnum.BAR)

    def test_str(self):
        self.assertEqual(str(SomeEnum.FOO), "foo")
        self.assertEqual(str(SomeEnum.BAR), "bar")
