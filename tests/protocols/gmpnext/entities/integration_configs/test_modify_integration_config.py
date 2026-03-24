#  SPDX-FileCopyrightText: 2026 Greenbone AG
#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from gvm.errors import RequiredArgument


class GmpModifyIntegrationConfigTestMixin:
    def test_modify_integration_config(self):
        self.gmp.modify_integration_config(integration_config_id="ic1")

        self.connection.send.has_been_called_with(
            b'<modify_integration_config uuid="ic1">'
            b"<service>"
            b"<url/>"
            b"<cacert/>"
            b"</service>"
            b"<oidc>"
            b"<oidc_provider_url/>"
            b"<client>"
            b"<id/>"
            b"<secret/>"
            b"</client>"
            b"</oidc>"
            b"</modify_integration_config>"
        )

    def test_modify_integration_config_missing_integration_config_id(self):
        with self.assertRaises(RequiredArgument):
            self.gmp.modify_integration_config(integration_config_id=None)

        with self.assertRaises(RequiredArgument):
            self.gmp.modify_integration_config(integration_config_id="")

    def test_modify_integration_config_with_service_url(self):
        self.gmp.modify_integration_config(
            integration_config_id="ic1",
            service_url="https://service.example.com",
        )

        self.connection.send.has_been_called_with(
            b'<modify_integration_config uuid="ic1">'
            b"<service>"
            b"<url>https://service.example.com</url>"
            b"<cacert/>"
            b"</service>"
            b"<oidc>"
            b"<oidc_provider_url/>"
            b"<client>"
            b"<id/>"
            b"<secret/>"
            b"</client>"
            b"</oidc>"
            b"</modify_integration_config>"
        )

    def test_modify_integration_config_with_service_cacert(self):
        self.gmp.modify_integration_config(
            integration_config_id="ic1",
            service_cacert="-----BEGIN CERTIFICATE-----foo-----END CERTIFICATE-----",
        )

        self.connection.send.has_been_called_with(
            b'<modify_integration_config uuid="ic1">'
            b"<service>"
            b"<url/>"
            b"<cacert>-----BEGIN CERTIFICATE-----foo-----END CERTIFICATE-----</cacert>"
            b"</service>"
            b"<oidc>"
            b"<oidc_provider_url/>"
            b"<client>"
            b"<id/>"
            b"<secret/>"
            b"</client>"
            b"</oidc>"
            b"</modify_integration_config>"
        )

    def test_modify_integration_config_with_oidc_provider_url(self):
        self.gmp.modify_integration_config(
            integration_config_id="ic1",
            oidc_provider_url="https://oidc.example.com",
        )

        self.connection.send.has_been_called_with(
            b'<modify_integration_config uuid="ic1">'
            b"<service>"
            b"<url/>"
            b"<cacert/>"
            b"</service>"
            b"<oidc>"
            b"<oidc_provider_url>https://oidc.example.com</oidc_provider_url>"
            b"<client>"
            b"<id/>"
            b"<secret/>"
            b"</client>"
            b"</oidc>"
            b"</modify_integration_config>"
        )

    def test_modify_integration_config_with_oidc_provider_client_id(self):
        self.gmp.modify_integration_config(
            integration_config_id="ic1",
            oidc_provider_client_id="client-id-1",
        )

        self.connection.send.has_been_called_with(
            b'<modify_integration_config uuid="ic1">'
            b"<service>"
            b"<url/>"
            b"<cacert/>"
            b"</service>"
            b"<oidc>"
            b"<oidc_provider_url/>"
            b"<client>"
            b"<id>client-id-1</id>"
            b"<secret/>"
            b"</client>"
            b"</oidc>"
            b"</modify_integration_config>"
        )

    def test_modify_integration_config_with_oidc_provider_client_secret(self):
        self.gmp.modify_integration_config(
            integration_config_id="ic1",
            oidc_provider_client_secret="secret-1",
        )

        self.connection.send.has_been_called_with(
            b'<modify_integration_config uuid="ic1">'
            b"<service>"
            b"<url/>"
            b"<cacert/>"
            b"</service>"
            b"<oidc>"
            b"<oidc_provider_url/>"
            b"<client>"
            b"<id/>"
            b"<secret>secret-1</secret>"
            b"</client>"
            b"</oidc>"
            b"</modify_integration_config>"
        )

    def test_modify_integration_config_with_all_fields(self):
        self.gmp.modify_integration_config(
            integration_config_id="ic1",
            service_url="https://service.example.com",
            service_cacert="cacert-data",
            oidc_provider_url="https://oidc.example.com",
            oidc_provider_client_id="client-id-1",
            oidc_provider_client_secret="secret-1",
        )

        self.connection.send.has_been_called_with(
            b'<modify_integration_config uuid="ic1">'
            b"<service>"
            b"<url>https://service.example.com</url>"
            b"<cacert>cacert-data</cacert>"
            b"</service>"
            b"<oidc>"
            b"<oidc_provider_url>https://oidc.example.com</oidc_provider_url>"
            b"<client>"
            b"<id>client-id-1</id>"
            b"<secret>secret-1</secret>"
            b"</client>"
            b"</oidc>"
            b"</modify_integration_config>"
        )
