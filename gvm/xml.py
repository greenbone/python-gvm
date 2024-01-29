# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys
from io import IOBase
from typing import List, Optional, Union

import defusedxml.lxml as secET
from defusedxml import DefusedXmlException
from lxml.etree import Element, LxmlError, SubElement, XMLParser
from lxml.etree import iselement as isxmlelement
from lxml.etree import tostring as xmltostring

from gvm.errors import GvmError, InvalidArgumentType


def create_parser():
    # huge_tree => disable security restrictions and support very deep trees and
    #              very long text content (for get_reports)
    return XMLParser(encoding="utf-8", huge_tree=True)


class XmlCommandElement:
    def __init__(self, element):
        self._element = element

    def add_element(
        self,
        name: str,
        text: Optional[str] = None,
        *,
        attrs: Optional[dict] = None,
    ):
        node = SubElement(self._element, name, attrib=attrs)
        node.text = text
        return XmlCommandElement(node)

    def set_attribute(self, name: str, value: str):
        self._element.set(name, value)

    def set_attributes(self, attrs: dict):
        """Set several attributes at once.

        Arguments:
            attrs (dict): Attributes to be set on the element
        """
        for key, value in attrs.items():
            self._element.set(key, value)

    def append_xml_str(self, xml_text: str):
        """Append a xml element in string format."""
        node = secET.fromstring(xml_text)
        self._element.append(node)

    def to_string(self) -> str:
        return xmltostring(self._element).decode("utf-8")

    def __str__(self):
        return self.to_string()


class XmlCommand(XmlCommandElement):
    def __init__(self, name):
        super().__init__(Element(name))


def pretty_print(
    xml: Union[str, List[Union[Element, str]], Element],
    file: IOBase = sys.stdout,
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
    if not isinstance(file, IOBase):
        raise TypeError(
            f"Type needs to be from IOBase, not {type(file)}."
        ) from None

    if isinstance(xml, list):
        for item in xml:
            if isxmlelement(item):
                file.write(
                    xmltostring(item, pretty_print=True).decode(
                        sys.getdefaultencoding() + "\n"
                    )
                )
            else:
                file.write(item + "\n")
    elif isxmlelement(xml):
        file.write(
            xmltostring(xml, pretty_print=True).decode(
                sys.getdefaultencoding() + "\n"
            )
        )
    elif isinstance(xml, str):
        tree = secET.fromstring(xml)
        file.write(
            xmltostring(tree, pretty_print=True).decode(
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
