# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys
from io import IOBase
from typing import AnyStr, List, Optional, TextIO, Union

import defusedxml.lxml as secET
from defusedxml import DefusedXmlException
from lxml.etree import Element as create_element
from lxml.etree import Error as EtreeError
from lxml.etree import LxmlError, SubElement, XMLParser
from lxml.etree import _Element as Element
from lxml.etree import iselement as is_xml_element
from lxml.etree import tostring as xml_to_string

from gvm.errors import GvmError, InvalidArgumentType

__all__ = (
    "Element",
    "create_parser",
    "parse_xml",
    "XmlCommandElement",
    "XmlCommand",
    "pretty_print",
    "validate_xml_string",
)


class XmlError(GvmError):
    pass


def create_parser():
    # huge_tree => disable security restrictions and support very deep trees and
    #              very long text content (for get_reports)
    return XMLParser(encoding="utf-8", huge_tree=True)


def parse_xml(xml: AnyStr) -> Element:
    parser = create_parser()
    try:
        parser.feed(xml)
        return parser.close()
    except EtreeError as e:
        raise XmlError(f"Invalid XML {xml!r}. Error was {e}") from e


class XmlCommandElement:
    def __init__(self, element: Element):
        self._element = element

    def add_element(
        self,
        name: str,
        text: Optional[str] = None,
        *,
        attrs: Optional[dict] = None,
    ) -> "XmlCommandElement":
        node = SubElement(self._element, name, attrib=attrs)
        node.text = text
        return XmlCommandElement(node)

    def set_attribute(self, name: str, value: str) -> "XmlCommandElement":
        self._element.set(name, value)
        return self

    def set_attributes(self, attrs: dict[str, str]) -> "XmlCommandElement":
        """Set several attributes at once.

        Arguments:
            attrs (dict): Attributes to be set on the element
        """
        for key, value in attrs.items():
            self._element.set(key, value)

        return self

    def append_xml_str(self, xml_text: str) -> None:
        """Append a xml element in string format."""
        node = secET.fromstring(xml_text)
        self._element.append(node)

    def to_string(self) -> str:
        return self.to_bytes().decode("utf-8")

    def to_bytes(self) -> bytes:
        return xml_to_string(self._element)

    def __str__(self) -> str:
        return self.to_string()

    def __bytes__(self) -> bytes:
        return self.to_bytes()


class XmlCommand(XmlCommandElement):
    def __init__(self, name: str) -> None:
        super().__init__(create_element(name))

    def add_filter(
        self,
        filter_string: Optional[str],
        filter_id: Optional[str],
    ) -> "XmlCommand":
        if filter_string:
            self.set_attribute("filter", filter_string)

        if filter_id:
            self.set_attribute("filt_id", filter_id)

        return self


def pretty_print(
    xml: Union[str, List[Union[Element, str]], Element],
    file: Union[TextIO, IOBase] = sys.stdout,
):
    """Prints beautiful XML-Code

    This function gets a string containing the xml, an object of
    List[lxml.etree.Element] or directly a lxml element.

    Print it with good readable format.

    Arguments:
        xml (str, List[lxml.etree.Element] or lxml.etree.Element):
            xml as string,
            List[lxml.etree.Element] or directly a lxml element.
        file:
            A IOBase type. Can be a File, StringIO, ...

    """
    if not isinstance(file, (IOBase, TextIO)):
        raise TypeError(
            f"Type needs to be from IOBase or TextIO, not {type(file)}."
        ) from None

    if isinstance(xml, list):
        for item in xml:
            if is_xml_element(item):
                file.write(
                    xml_to_string(item, pretty_print=True).decode(
                        sys.getdefaultencoding() + "\n"
                    )
                )
            else:
                file.write(str(item) + "\n")
    elif is_xml_element(xml):
        file.write(
            xml_to_string(xml, pretty_print=True).decode(
                sys.getdefaultencoding() + "\n"
            )
        )
    elif isinstance(xml, str):
        tree = secET.fromstring(xml)
        file.write(
            xml_to_string(tree, pretty_print=True).decode(
                sys.getdefaultencoding() + "\n"
            )
        )
    else:
        raise InvalidArgumentType(
            function=pretty_print.__name__, argument="xml", arg_type=""
        )


def validate_xml_string(xml_string: str):
    """Checks if the passed string contains valid XML

    Raises a GvmError if the XML is invalid. Otherwise the function just
    returns.

    Arguments:
        xml_string: XML string to validate

    Raises:
        GvmError: The xml string did contain invalid XML

    """
    try:
        secET.fromstring(xml_string)
    except (DefusedXmlException, LxmlError) as e:
        raise GvmError("Invalid XML", e) from e
