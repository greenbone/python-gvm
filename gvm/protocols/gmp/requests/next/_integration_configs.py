from typing import Optional

from gvm.errors import RequiredArgument
from gvm.protocols.core import Request
from gvm.protocols.gmp.requests import EntityID
from gvm.utils import to_bool
from gvm.xml import XmlCommand


class IntegrationConfigs:
    @classmethod
    def get_integration_config(
        cls, integration_config_id: EntityID, *, details: Optional[bool] = None
    ) -> Request:
        """Request a single Integration Configuration.

        Args:
            integration_config_id: UUID of the integration config to request.
            details: Whether to include detail information.
        """
        if not integration_config_id:
            raise RequiredArgument(
                function=cls.get_integration_config.__name__,
                argument="integration_config_id",
            )

        cmd = XmlCommand("get_integration_configs")
        cmd.set_attribute("integration_config_id", str(integration_config_id))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return cmd

    @classmethod
    def get_integration_configs(
        cls,
        *,
        filter_string: Optional[str] = None,
        filter_id: Optional[EntityID] = None,
    ) -> Request:
        """Request a list of Integration Configurations.

        Args:
            filter_string: Filter term to use for the query.
            filter_id: UUID of an existing filter to use for the query.
        """
        cmd = XmlCommand("get_integration_configs")
        cmd.add_filter(filter_string, filter_id)

        return cmd

    @classmethod
    def modify_integration_config(
        cls,
        integration_config_id: EntityID,
        *,
        service_url: Optional[str] = None,
        service_cacert: Optional[str] = None,
        oidc_provider_url: Optional[str] = None,
        oidc_provider_client_id: Optional[str] = None,
        oidc_provider_client_secret: Optional[str] = None,
    ) -> Request:
        """Modify an existing Integration Configuration.

        Args:
            integration_config_id: UUID of configuration to modify.
            service_url: Integration Service URL.
            service_cacert: Integration Service Certificate.
            oidc_provider_url: OIDC Provider URL.
            oidc_provider_client_id: OIDC Provider Client ID.
            oidc_provider_client_secret: OIDC Provider Client Secret.
        """
        if not integration_config_id:
            raise RequiredArgument(
                function=cls.modify_integration_config.__name__,
                argument="integration_config_id",
            )

        cmd = XmlCommand("modify_integration_config")
        cmd.set_attribute("uuid", str(integration_config_id))

        # <service> element
        service = cmd.add_element("service")

        if service_url is not None:
            service.add_element("url", service_url)
        else:
            service.add_element("url")
        if service_cacert is not None:
            service.add_element("cacert", service_cacert)
        else:
            service.add_element("cacert")

        # <oidc> element
        oidc = cmd.add_element("oidc")
        if oidc_provider_url is not None:
            oidc.add_element("oidc_provider_url", oidc_provider_url)
        else:
            oidc.add_element("oidc_provider_url")

        oidc_client = oidc.add_element("client")
        if oidc_provider_client_id is not None:
            oidc_client.add_element("id", oidc_provider_client_id)
        else:
            oidc_client.add_element("id")
        if oidc_provider_client_secret is not None:
            oidc_client.add_element("secret", oidc_provider_client_secret)
        else:
            oidc_client.add_element("secret")

        return cmd
