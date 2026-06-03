from enum import Enum

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests._entity_id import EntityID
from gvm.xml import XmlCommand


class AgentInstallerInstructionLanguageType(Enum):
    EN = "en"
    DE = "de"


class AgentInstallerInstructions:
    @classmethod
    def get_agent_installer_instruction(
        cls,
        scanner_id: EntityID,
        language_type: AgentInstallerInstructionLanguageType,
    ) -> Request:
        """Request an agent installer instruction.

        Args:
            scanner_id: UUID of the Agent controller to get the installer instruction for.
            language_type: Language of the installer instruction.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=cls.get_agent_installer_instruction.__name__,
                argument="scanner_id",
            )

        if not language_type:
            raise RequiredArgument(
                function=cls.get_agent_installer_instruction.__name__,
                argument="language_type",
            )

        cmd = XmlCommand("get_agent_installer_instruction")
        cmd.set_attribute("scanner_id", str(scanner_id))
        cmd.set_attribute("language", language_type.value)

        return cmd
