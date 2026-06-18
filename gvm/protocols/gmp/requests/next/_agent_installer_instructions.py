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
        origin_url: str,
    ) -> Request:
        """Request an agent installer instruction.

        Args:
            scanner_id: UUID of the Agent controller to get the installer instruction for.
            language_type: Language of the installer instruction.
            origin_url: Origin URL used to generate the executable agent
                installation command.

        Raises:
            RequiredArgument: If scanner_id, language_type, or origin_url is
                missing.
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

        if not origin_url:
            raise RequiredArgument(
                function=cls.get_agent_installer_instruction.__name__,
                argument="origin_url",
            )

        cmd = XmlCommand("get_agent_installer_instruction")
        cmd.set_attribute("scanner_id", str(scanner_id))
        cmd.set_attribute("language", language_type.value)
        cmd.set_attribute("origin_url", origin_url)

        return cmd
