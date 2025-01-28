# SPDX-FileCopyrightText: 2018-2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys
from io import IOBase
from typing import AnyStr, Optional, TextIO, Union
from uuid import UUID

from lxml.etree import DocInfo, SubElement, XMLParser
from lxml.etree import Element as create_element
from lxml.etree import Error as EtreeError
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
)


class XmlError(GvmError):
    pass


def check_xml_document(
    root_element: Element,
    forbid_dtd: bool = False,
    forbid_entities: bool = True,
) -> None:
    """
    Check an element for DTD and entity declarations
    """
    doc_info: DocInfo = root_element.getroottree().docinfo
    if doc_info.doctype:  # type: ignore
        if forbid_dtd:
            raise XmlError(
                "XML document contains a forbidden DTD declaration "
                f"{doc_info.system_url} {doc_info.public_id}"  # type: ignore
            )

    if forbid_entities:
        for dtd in doc_info.internalDTD, doc_info.externalDTD:
            if dtd is None:
                continue
            for entity in dtd.iterentities():  # type: ignore
                raise XmlError(
                    f"XML Document contains forbidden entity declaration "
                    f"{entity.name} {entity.content}"
                )


def create_parser():
    # huge_tree => disable security restrictions and support very deep trees and
    #              very long text content (for get_reports)
    # resolve_entities=False => disable entity resolution for security reasons
    return XMLParser(encoding="utf-8", huge_tree=True, resolve_entities=False)


def parse_xml(xml: AnyStr) -> Element:
    """
    Parse an XML string and return the root element

    Raises an XmlError if the XML is invalid.
    """
    parser = create_parser()
    try:
        parser.feed(xml)
        element = parser.close()
        check_xml_document(element)
        return element
    except EtreeError as e:
        raise XmlError(f"Invalid XML {xml!r}. Error was {e}") from e


class XmlCommandElement:
    """
    Base class for XML commands

    It's used to create XML command requests for the XML based protocols.
    """

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
        """Set an attribute on the element.

        Args:
            name: Name of the attribute
            value: Value of the attribute
        """
        self._element.set(name, value)
        return self

    def set_attributes(self, attrs: dict[str, str]) -> "XmlCommandElement":
        """Set several attributes at once.

        Args:
            attrs: Attributes to be set on the element
        """
        for key, value in attrs.items():
            self._element.set(key, value)

        return self

    def set_text(self, text: Optional[str]) -> "XmlCommandElement":
        """Set the text of the element.

        Args:
            text: Text to be set on the element. None to remove the text.
        """
        self._element.text = text
        return self

    def append_xml_str(self, xml_text: str) -> None:
        """Append a xml element in string format."""
        node = parse_xml(xml_text)
        self._element.append(node)

    def to_string(self, *, encoding: str = "utf-8") -> str:
        """
        Convert the XML element to a string

        Args:
            encoding: The encoding to use for the string. Default is 'utf-8'.
        """
        return self.to_bytes().decode(encoding)

    def to_bytes(self) -> bytes:
        """
        Convert the XML element to a bytes object
        """
        return xml_to_string(self._element)

    def __str__(self) -> str:
        """
        Convert the XML element to a string using the default encoding.
        """
        return self.to_string()

    def __bytes__(self) -> bytes:
        """
        Convert the XML element to a bytes object
        """
        return self.to_bytes()


class XmlCommand(XmlCommandElement):
    """
    Class to create XML commands
    """

    def __init__(self, name: str) -> None:
        """
        Create a new XML command

        Args:
            name: The name of the root element of the command.
        """
        super().__init__(create_element(name))

    def add_filter(
        self,
        filter_string: Optional[str],
        filter_id: Optional[Union[str, UUID]],
    ) -> "XmlCommand":
        """
        Add a filter to the command.

        Args:
            filter_string: The filter string to be added.
            filter_id: The filter ID to be added.
        """
        if filter_string:
            self.set_attribute("filter", filter_string)

        if filter_id:
            self.set_attribute("filt_id", str(filter_id))

        return self


def pretty_print(
    xml: Union[str, list[Union[Element, str]], Element],
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
        tree = parse_xml(xml)
        file.write(
            xml_to_string(tree, pretty_print=True).decode(
                sys.getdefaultencoding() + "\n"
            )
        )
    else:
        raise InvalidArgumentType(
            function=pretty_print.__name__, argument="xml", arg_type=""
        )
