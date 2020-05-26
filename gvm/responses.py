from gvm.classes import *
from gvm.resolve import *
from dataclasses import dataclass
from lxml import etree


@dataclass
class Response:
    """
    standard Python Response Object
    """

    response_name: str
    status: int
    status_text: str

    def __init__(self, response_name: str, status: int, status_text: str):
        self.response_name = response_name
        self.status = status
        self.status_text = status_text


@dataclass
class AuthenticateResponse(Response):
    """
    Response Object for authenticate command
    """

    role: Role
    timezone: str
    severity: str

    def __init__(self, root: etree.Element):
        super().__init__(root.tag, root.get("status"), root.get("status_text"))
        self.role = resolve_role(root.find("role"))
        self.timezone = root.find("timezone").text
        self.severity = root.find("severity").text


@dataclass
class GetPortListsResponse(Response):
    """
    Response Object for a get_port_lists command
    """

    port_lists: list

    def __init__(self, root: etree.Element):
        super().__init__(root.tag, root.get("status"), root.get("status_text"))
        self.port_lists = resolve_port_lists(root)


CLASSDICT = {
    "authenticate_response": AuthenticateResponse,
    "get_port_lists_response": GetPortListsResponse
}
