# -*- coding: utf-8 -*-
# Copyright (C) 2018-2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=arguments-differ, redefined-builtin, too-many-lines

"""
Module for communication with gvmd in
`Greenbone Management Protocol version 20.08`_

.. _Greenbone Management Protocol version 20.08:
    https://docs.greenbone.net/API/GMP/gmp-20.08.html
"""
import logging
from numbers import Integral

from typing import Any, List, Optional, Callable, Union
from lxml import etree

from gvm.connections import GvmConnection
from gvm.errors import InvalidArgument, InvalidArgumentType, RequiredArgument
from gvm.protocols.base import GvmProtocol
from gvm.protocols.gmpv208.entities.report_formats import (
    ReportFormatType,
)
from gvm.utils import (
    check_command_status,
    to_base64,
    to_bool,
    to_comma_list,
    add_filter,
)
from gvm.xml import XmlCommand

from . import types
from .types import *  # pylint: disable=unused-wildcard-import, wildcard-import


PROTOCOL_VERSION = (20, 8)


logger = logging.getLogger(__name__)


class GmpV208Mixin(GvmProtocol):
    """Python interface for Greenbone Management Protocol

    This class implements the `Greenbone Management Protocol version 20.08`_

    Arguments:
        connection: Connection to use to talk with the gvmd daemon. See
            :mod:`gvm.connections` for possible connection types.
        transform: Optional transform `callable`_ to convert response data.
            After each request the callable gets passed the plain response data
            which can be used to check the data and/or conversion into different
            representations like a xml dom.

            See :mod:`gvm.transforms` for existing transforms.

    .. _Greenbone Management Protocol version 20.08:
        https://docs.greenbone.net/API/GMP/gmp-20.08.html
    .. _callable:
        https://docs.python.org/3/library/functions.html#callable
    """

    types = types

    def __init__(
        self,
        connection: GvmConnection,
        *,
        transform: Optional[Callable[[str], Any]] = None,
    ):
        super().__init__(connection, transform=transform)

        # Is authenticated on gvmd
        self._authenticated = False

    def is_authenticated(self) -> bool:
        """Checks if the user is authenticated

        If the user is authenticated privileged GMP commands like get_tasks
        may be send to gvmd.

        Returns:
            bool: True if an authenticated connection to gvmd has been
            established.
        """
        return self._authenticated

    def authenticate(self, username: str, password: str) -> Any:
        """Authenticate to gvmd.

        The generated authenticate command will be send to server.
        Afterwards the response is read, transformed and returned.

        Arguments:
            username: Username
            password: Password

        Returns:
            Transformed response from server.
        """
        cmd = XmlCommand("authenticate")

        if not username:
            raise RequiredArgument(
                function=self.authenticate.__name__, argument='username'
            )

        if not password:
            raise RequiredArgument(
                function=self.authenticate.__name__, argument='password'
            )

        credentials = cmd.add_element("credentials")
        credentials.add_element("username", username)
        credentials.add_element("password", password)

        self._send(cmd.to_string())
        response = self._read()

        if check_command_status(response):
            self._authenticated = True

        return self._transform(response)

    def create_permission(
        self,
        name: str,
        subject_id: str,
        subject_type: PermissionSubjectType,
        *,
        resource_id: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new permission

        Arguments:
            name: Name of the new permission
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            comment: Comment for the permission
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_permission.__name__, argument='name'
            )

        if not subject_id:
            raise RequiredArgument(
                function=self.create_permission.__name__, argument='subject_id'
            )

        if not isinstance(subject_type, PermissionSubjectType):
            raise InvalidArgumentType(
                function=self.create_permission.__name__,
                argument='subject_type',
                arg_type=PermissionSubjectType.__name__,
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("name", name)

        _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
        _xmlsubject.add_element("type", subject_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=self.create_permission.__name__,
                    argument='resource_id',
                )

            if not resource_type:
                raise RequiredArgument(
                    function=self.create_permission.__name__,
                    argument='resource_type',
                )

            if not isinstance(resource_type, self.types.EntityType):
                raise InvalidArgumentType(
                    function=self.create_permission.__name__,
                    argument='resource_type',
                    arg_type=self.types.EntityType.__name__,
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )

            _actual_resource_type = resource_type
            if resource_type.value == EntityType.AUDIT.value:
                _actual_resource_type = EntityType.TASK
            elif resource_type.value == EntityType.POLICY.value:
                _actual_resource_type = EntityType.SCAN_CONFIG

            _xmlresource.add_element("type", _actual_resource_type.value)

        return self._send_xml_command(cmd)

    def create_tag(
        self,
        name: str,
        resource_type: EntityType,
        *,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[List[str]] = None,
        value: Optional[str] = None,
        comment: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> Any:
        """Create a tag.

        Arguments:
            name: Name of the tag. A full tag name consisting of namespace and
                predicate e.g. `foo:bar`.
            resource_type: Entity type the tag is to be attached to.
            resource_filter: Filter term to select resources the tag is to be
                attached to. Only one of resource_filter or resource_ids can be
                provided.
            resource_ids: IDs of the resources the tag is to be attached to.
                Only one of resource_filter or resource_ids can be provided.
            value: Value associated with the tag.
            comment: Comment for the tag.
            active: Whether the tag should be active.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_tag.__name__, argument='name'
            )

        if resource_filter and resource_ids:
            raise InvalidArgument(
                "create_tag accepts either resource_filter or resource_ids "
                "argument",
                function=self.create_tag.__name__,
            )

        if not resource_type:
            raise RequiredArgument(
                function=self.create_tag.__name__, argument='resource_type'
            )

        if not isinstance(resource_type, self.types.EntityType):
            raise InvalidArgumentType(
                function=self.create_tag.__name__,
                argument='resource_type',
                arg_type=EntityType.__name__,
            )

        cmd = XmlCommand('create_tag')
        cmd.add_element('name', name)

        _xmlresources = cmd.add_element("resources")
        if resource_filter is not None:
            _xmlresources.set_attribute("filter", resource_filter)

        for resource_id in resource_ids or []:
            _xmlresources.add_element(
                "resource", attrs={"id": str(resource_id)}
            )

        _actual_resource_type = resource_type
        if resource_type.value == EntityType.AUDIT.value:
            _actual_resource_type = EntityType.TASK
        elif resource_type.value == EntityType.POLICY.value:
            _actual_resource_type = EntityType.SCAN_CONFIG
        _xmlresources.add_element("type", _actual_resource_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if value:
            cmd.add_element("value", value)

        if active is not None:
            if active:
                cmd.add_element("active", "1")
            else:
                cmd.add_element("active", "0")

        return self._send_xml_command(cmd)

    def get_aggregates(
        self,
        resource_type: EntityType,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        sort_criteria: Optional[list] = None,
        data_columns: Optional[list] = None,
        group_column: Optional[str] = None,
        subgroup_column: Optional[str] = None,
        text_columns: Optional[list] = None,
        first_group: Optional[int] = None,
        max_groups: Optional[int] = None,
        mode: Optional[int] = None,
        **kwargs,
    ) -> Any:
        """Request aggregated information on a resource / entity type

        Additional arguments can be set via the kwargs parameter for backward
        compatibility with older versions of python-gvm, but are not validated.

        Arguments:
            resource_type: The entity type to gather data from
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            sort_criteria: List of sort criteria (dicts that can contain
                a field, stat and order)
            data_columns: List of fields to aggregate data from
            group_column: The field to group the entities by
            subgroup_column: The field to further group the entities
                inside groups by
            text_columns: List of simple text columns which no statistics
                are calculated for
            first_group: The index of the first aggregate group to return
            max_groups: The maximum number of aggregate groups to return,
                -1 for all
            mode: Special mode for aggregation

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not resource_type:
            raise RequiredArgument(
                function=self.get_aggregates.__name__, argument='resource_type'
            )

        if not isinstance(resource_type, self.types.EntityType):
            raise InvalidArgumentType(
                function=self.get_aggregates.__name__,
                argument='resource_type',
                arg_type=self.types.EntityType.__name__,
            )

        cmd = XmlCommand('get_aggregates')

        _actual_resource_type = resource_type
        if resource_type.value == EntityType.AUDIT.value:
            _actual_resource_type = EntityType.TASK
            cmd.set_attribute('usage_type', 'audit')
        elif resource_type.value == EntityType.POLICY.value:
            _actual_resource_type = EntityType.SCAN_CONFIG
            cmd.set_attribute('usage_type', 'policy')
        elif resource_type.value == EntityType.SCAN_CONFIG.value:
            cmd.set_attribute('usage_type', 'scan')
        elif resource_type.value == EntityType.TASK.value:
            cmd.set_attribute('usage_type', 'scan')
        cmd.set_attribute('type', _actual_resource_type.value)

        add_filter(cmd, filter, filter_id)

        if first_group is not None:
            if not isinstance(first_group, int):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument='first_group',
                    arg_type=int.__name__,
                )
            cmd.set_attribute('first_group', str(first_group))

        if max_groups is not None:
            if not isinstance(max_groups, int):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument='max_groups',
                    arg_type=int.__name__,
                )
            cmd.set_attribute('max_groups', str(max_groups))

        if sort_criteria is not None:
            if not isinstance(sort_criteria, list):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument='sort_criteria',
                    arg_type=list.__name__,
                )
            for sort in sort_criteria:
                if not isinstance(sort, dict):
                    raise InvalidArgumentType(
                        function=self.get_aggregates.__name__,
                        argument='sort_criteria',
                    )

                sort_elem = cmd.add_element('sort')
                if sort.get('field'):
                    sort_elem.set_attribute('field', sort.get('field'))

                if sort.get('stat'):
                    if isinstance(sort['stat'], AggregateStatistic):
                        sort_elem.set_attribute('stat', sort['stat'].value)
                    else:
                        stat = get_aggregate_statistic_from_string(sort['stat'])
                        sort_elem.set_attribute('stat', stat.value)

                if sort.get('order'):
                    if isinstance(sort['order'], SortOrder):
                        sort_elem.set_attribute('order', sort['order'].value)
                    else:
                        so = get_sort_order_from_string(sort['order'])
                        sort_elem.set_attribute('order', so.value)

        if data_columns is not None:
            if not isinstance(data_columns, list):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument='data_columns',
                    arg_type=list.__name__,
                )
            for column in data_columns:
                cmd.add_element('data_column', column)

        if group_column is not None:
            cmd.set_attribute('group_column', group_column)

        if subgroup_column is not None:
            if not group_column:
                raise RequiredArgument(
                    '{} requires a group_column argument'
                    ' if subgroup_column is given'.format(
                        self.get_aggregates.__name__
                    ),
                    function=self.get_aggregates.__name__,
                    argument='subgroup_column',
                )
            cmd.set_attribute('subgroup_column', subgroup_column)

        if text_columns is not None:
            if not isinstance(text_columns, list):
                raise InvalidArgumentType(
                    function=self.get_aggregates.__name__,
                    argument='text_columns',
                    arg_type=list.__name__,
                )
            for column in text_columns:
                cmd.add_element('text_column', column)

        if mode is not None:
            cmd.set_attribute('mode', mode)

        # Add additional keyword args as attributes for backward compatibility.
        cmd.set_attributes(kwargs)

        return self._send_xml_command(cmd)

    def modify_permission(
        self,
        permission_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        subject_id: Optional[str] = None,
        subject_type: Optional[PermissionSubjectType] = None,
    ) -> Any:
        """Modifies an existing permission.

        Arguments:
            permission_id: UUID of permission to be modified.
            comment: The comment on the permission.
            name: Permission name, currently the name of a command.
            subject_id: UUID of subject to whom the permission is granted
            subject_type: Type of the subject user, group or role
            resource_id: UUID of entity to which the permission applies
            resource_type: Type of the resource. For Super permissions user,
                group or role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.modify_permission.__name__,
                argument='permission_id',
            )

        cmd = XmlCommand("modify_permission")
        cmd.set_attribute("permission_id", permission_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if resource_id or resource_type:
            if not resource_id:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument='resource_id',
                )

            if not resource_type:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument='resource_type',
                )

            if not isinstance(resource_type, self.types.EntityType):
                raise InvalidArgumentType(
                    function=self.modify_permission.__name__,
                    argument='resource_type',
                    arg_type=self.types.EntityType.__name__,
                )

            _xmlresource = cmd.add_element(
                "resource", attrs={"id": resource_id}
            )
            _actual_resource_type = resource_type
            if resource_type.value == EntityType.AUDIT.value:
                _actual_resource_type = EntityType.TASK
            elif resource_type.value == EntityType.POLICY.value:
                _actual_resource_type = EntityType.SCAN_CONFIG
            _xmlresource.add_element("type", _actual_resource_type.value)

        if subject_id or subject_type:
            if not subject_id:
                raise RequiredArgument(
                    function=self.modify_permission.__name__,
                    argument='subject_id',
                )

            if not isinstance(subject_type, PermissionSubjectType):
                raise InvalidArgumentType(
                    function=self.modify_permission.__name__,
                    argument='subject_type',
                    arg_type=PermissionSubjectType.__name__,
                )

            _xmlsubject = cmd.add_element("subject", attrs={"id": subject_id})
            _xmlsubject.add_element("type", subject_type.value)

        return self._send_xml_command(cmd)

    def modify_tag(
        self,
        tag_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        value=None,
        active=None,
        resource_action: Optional[str] = None,
        resource_type: Optional[EntityType] = None,
        resource_filter: Optional[str] = None,
        resource_ids: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing tag.

        Arguments:
            tag_id: UUID of the tag.
            comment: Comment to add to the tag.
            name: Name of the tag.
            value: Value of the tag.
            active: Whether the tag is active.
            resource_action: Whether to add or remove resources instead of
                overwriting. One of '', 'add', 'set' or 'remove'.
            resource_type: Type of the resources to which to attach the tag.
                Required if resource_filter is set.
            resource_filter: Filter term to select resources the tag is to be
                attached to.
            resource_ids: IDs of the resources to which to attach the tag.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.modify_tag.__name__, argument='tag_id'
            )

        cmd = XmlCommand("modify_tag")
        cmd.set_attribute("tag_id", str(tag_id))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if value:
            cmd.add_element("value", value)

        if active is not None:
            cmd.add_element("active", to_bool(active))

        if resource_action or resource_filter or resource_ids or resource_type:
            if resource_filter and not resource_type:
                raise RequiredArgument(
                    function=self.modify_tag.__name__, argument='resource_type'
                )

            _xmlresources = cmd.add_element("resources")
            if resource_action is not None:
                _xmlresources.set_attribute("action", resource_action)

            if resource_filter is not None:
                _xmlresources.set_attribute("filter", resource_filter)

            for resource_id in resource_ids or []:
                _xmlresources.add_element(
                    "resource", attrs={"id": str(resource_id)}
                )

            if resource_type is not None:
                if not isinstance(resource_type, self.types.EntityType):
                    raise InvalidArgumentType(
                        function=self.modify_tag.__name__,
                        argument="resource_type",
                        arg_type=EntityType.__name__,
                    )
                _actual_resource_type = resource_type
                if resource_type.value == EntityType.AUDIT.value:
                    _actual_resource_type = EntityType.TASK
                elif resource_type.value == EntityType.POLICY.value:
                    _actual_resource_type = EntityType.SCAN_CONFIG
                _xmlresources.add_element("type", _actual_resource_type.value)

        return self._send_xml_command(cmd)

    def clone_ticket(self, ticket_id: str) -> Any:
        """Clone an existing ticket

        Arguments:
            ticket_id: UUID of an existing ticket to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.clone_ticket.__name__, argument='ticket_id'
            )

        cmd = XmlCommand("create_ticket")

        _copy = cmd.add_element("copy", ticket_id)

        return self._send_xml_command(cmd)

    def get_feed(self, feed_type: Optional[FeedType]) -> Any:
        """Request a single feed

        Arguments:
            feed_type: Type of single feed to get: NVT, CERT or SCAP

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not feed_type:
            raise RequiredArgument(
                function=self.get_feed.__name__, argument='feed_type'
            )

        if not isinstance(feed_type, FeedType):
            raise InvalidArgumentType(
                function=self.get_feed.__name__,
                argument='feed_type',
                arg_type=FeedType.__name__,
            )

        cmd = XmlCommand("get_feeds")
        cmd.set_attribute("type", feed_type.value)

        return self._send_xml_command(cmd)

    def create_credential(
        self,
        name: str,
        credential_type: CredentialType,
        *,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        certificate: Optional[str] = None,
        key_phrase: Optional[str] = None,
        private_key: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        auth_algorithm: Optional[SnmpAuthAlgorithm] = None,
        community: Optional[str] = None,
        privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None,
        privacy_password: Optional[str] = None,
        public_key: Optional[str] = None,
    ) -> Any:
        """Create a new credential

        Create a new credential e.g. to be used in the method of an alert.

        Currently the following credential types are supported:

            - Username + Password
            - Username + SSH-Key
            - Client Certificates
            - SNMPv1 or SNMPv2c protocol
            - S/MIME Certificate
            - OpenPGP Key
            - Password only

        Arguments:
            name: Name of the new credential
            credential_type: The credential type.
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential.
                Required for client-certificate and smime credential types.
            key_phrase: Key passphrase for the private key.
                Used for the username+ssh-key credential type.
            private_key: Private key to use for login. Required
                for usk credential type. Also used for the cc credential type.
                The supported key types (dsa, rsa, ecdsa, ...) and formats (PEM,
                PKC#12, OpenSSL, ...) depend on your installed GnuTLS version.
            login: Username for the credential. Required for username+password,
                username+ssh-key and snmp credential type.
            password: Password for the credential. Used for username+password
                and snmp credential types.
            community: The SNMP community
            auth_algorithm: The SNMP authentication algorithm. Required for snmp
                credential type.
            privacy_algorithm: The SNMP privacy algorithm
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format. Required
                for pgp credential type.

        Examples:
            Creating a Username + Password credential

            .. code-block:: python

                gmp.create_credential(
                    name='UP Credential',
                    credential_type=CredentialType.USERNAME_PASSWORD,
                    login='foo',
                    password='bar',
                )

            Creating a Username + SSH Key credential

            .. code-block:: python

                with open('path/to/private-ssh-key') as f:
                    key = f.read()

                gmp.create_credential(
                    name='USK Credential',
                    credential_type=CredentialType.USERNAME_SSH_KEY,
                    login='foo',
                    key_phrase='foobar',
                    private_key=key,
                )

            Creating a PGP credential

            .. note::

                A compatible public pgp key file can be exported with GnuPG via
                ::

                    $ gpg --armor --export alice@cyb.org > alice.asc

            .. code-block:: python

                with open('path/to/pgp.key.asc') as f:
                    key = f.read()

                gmp.create_credential(
                    name='PGP Credential',
                    credential_type=CredentialType.PGP_ENCRYPTION_KEY,
                    public_key=key,
                )

            Creating a S/MIME credential

            .. code-block:: python

                with open('path/to/smime-cert') as f:
                    cert = f.read()

                gmp.create_credential(
                    name='SMIME Credential',
                    credential_type=CredentialType.SMIME_CERTIFICATE,
                    certificate=cert,
                )

            Creating a Password-Only credential

            .. code-block:: python

                gmp.create_credential(
                    name='Password-Only Credential',
                    credential_type=CredentialType.PASSWORD_ONLY,
                    password='foo',
                )
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_credential.__name__, argument='name'
            )

        if not isinstance(credential_type, self.types.CredentialType):
            raise InvalidArgumentType(
                function=self.create_credential.__name__,
                argument='credential_type',
                arg_type=CredentialType.__name__,
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("name", name)

        cmd.add_element("type", credential_type.value)

        if comment:
            cmd.add_element("comment", comment)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", to_bool(allow_insecure))

        if (
            credential_type == CredentialType.CLIENT_CERTIFICATE
            or credential_type == CredentialType.SMIME_CERTIFICATE
        ):
            if not certificate:
                raise RequiredArgument(
                    function=self.create_credential.__name__,
                    argument='certificate',
                )

            cmd.add_element("certificate", certificate)

        if (
            credential_type == CredentialType.USERNAME_PASSWORD
            or credential_type == CredentialType.USERNAME_SSH_KEY
            or credential_type == CredentialType.SNMP
        ):
            if not login:
                raise RequiredArgument(
                    function=self.create_credential.__name__, argument='login'
                )

            cmd.add_element("login", login)

        if credential_type == CredentialType.PASSWORD_ONLY and not password:
            raise RequiredArgument(
                function=self.create_credential.__name__, argument='password'
            )

        if (
            credential_type == CredentialType.USERNAME_PASSWORD
            or credential_type == CredentialType.SNMP
            or credential_type == CredentialType.PASSWORD_ONLY
        ) and password:
            cmd.add_element("password", password)

        if credential_type == CredentialType.USERNAME_SSH_KEY:
            if not private_key:
                raise RequiredArgument(
                    function=self.create_credential.__name__,
                    argument='private_key',
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

            if key_phrase:
                _xmlkey.add_element("phrase", key_phrase)

        if credential_type == CredentialType.CLIENT_CERTIFICATE and private_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("private", private_key)

        if credential_type == CredentialType.SNMP:
            if not isinstance(auth_algorithm, self.types.SnmpAuthAlgorithm):
                raise InvalidArgumentType(
                    function=self.create_credential.__name__,
                    argument='auth_algorithm',
                    arg_type=SnmpAuthAlgorithm.__name__,
                )

            cmd.add_element("auth_algorithm", auth_algorithm.value)

            if community:
                cmd.add_element("community", community)

            if privacy_algorithm is not None or privacy_password:
                _xmlprivacy = cmd.add_element("privacy")

                if privacy_algorithm is not None:
                    if not isinstance(
                        privacy_algorithm, self.types.SnmpPrivacyAlgorithm
                    ):
                        raise InvalidArgumentType(
                            function=self.create_credential.__name__,
                            argument='privacy_algorithm',
                            arg_type=SnmpPrivacyAlgorithm.__name__,
                        )

                    _xmlprivacy.add_element(
                        "algorithm", privacy_algorithm.value
                    )

                if privacy_password:
                    _xmlprivacy.add_element("password", privacy_password)

        if credential_type == CredentialType.PGP_ENCRYPTION_KEY:
            if not public_key:
                raise RequiredArgument(
                    function=self.create_credential.__name__,
                    argument='public_key',
                )

            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

        return self._send_xml_command(cmd)

    def modify_credential(
        self,
        credential_id: str,
        *,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        certificate: Optional[str] = None,
        key_phrase: Optional[str] = None,
        private_key: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        auth_algorithm: Optional[SnmpAuthAlgorithm] = None,
        community: Optional[str] = None,
        privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None,
        privacy_password: Optional[str] = None,
        public_key: Optional[str] = None,
    ) -> Any:
        """Modifies an existing credential.

        Arguments:
            credential_id: UUID of the credential
            name: Name of the credential
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential
            key_phrase: Key passphrase for the private key
            private_key: Private key to use for login
            login: Username for the credential
            password: Password for the credential
            auth_algorithm: The authentication algorithm for SNMP
            community: The SNMP community
            privacy_algorithm: The privacy algorithm for SNMP
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.modify_credential.__name__,
                argument='credential_id',
            )

        cmd = XmlCommand("modify_credential")
        cmd.set_attribute("credential_id", credential_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if allow_insecure is not None:
            cmd.add_element("allow_insecure", to_bool(allow_insecure))

        if certificate:
            cmd.add_element("certificate", certificate)

        if key_phrase and private_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("phrase", key_phrase)
            _xmlkey.add_element("private", private_key)
        elif (not key_phrase and private_key) or (
            key_phrase and not private_key
        ):
            raise RequiredArgument(
                function=self.modify_credential.__name__,
                argument='key_phrase and private_key',
            )

        if login:
            cmd.add_element("login", login)

        if password:
            cmd.add_element("password", password)

        if auth_algorithm:
            if not isinstance(auth_algorithm, self.types.SnmpAuthAlgorithm):
                raise InvalidArgumentType(
                    function=self.modify_credential.__name__,
                    argument='auth_algorithm',
                    arg_type=SnmpAuthAlgorithm.__name__,
                )
            cmd.add_element("auth_algorithm", auth_algorithm.value)

        if community:
            cmd.add_element("community", community)

        if privacy_algorithm is not None or privacy_password is not None:
            _xmlprivacy = cmd.add_element("privacy")

            if privacy_algorithm is not None:
                if not isinstance(
                    privacy_algorithm, self.types.SnmpPrivacyAlgorithm
                ):
                    raise InvalidArgumentType(
                        function=self.modify_credential.__name__,
                        argument='privacy_algorithm',
                        arg_type=SnmpPrivacyAlgorithm.__name__,
                    )

                _xmlprivacy.add_element("algorithm", privacy_algorithm.value)

            if privacy_password is not None:
                _xmlprivacy.add_element("password", privacy_password)

        if public_key:
            _xmlkey = cmd.add_element("key")
            _xmlkey.add_element("public", public_key)

        return self._send_xml_command(cmd)

    def create_ticket(
        self,
        *,
        result_id: str,
        assigned_to_user_id: str,
        note: str,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new ticket

        Arguments:
            result_id: UUID of the result the ticket applies to
            assigned_to_user_id: UUID of a user the ticket should be assigned to
            note: A note about opening the ticket
            comment: Comment for the ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not result_id:
            raise RequiredArgument(
                function=self.create_ticket.__name__, argument='result_id'
            )

        if not assigned_to_user_id:
            raise RequiredArgument(
                function=self.create_ticket.__name__,
                argument='assigned_to_user_id',
            )

        if not note:
            raise RequiredArgument(
                function=self.create_ticket.__name__, argument='note'
            )

        cmd = XmlCommand("create_ticket")

        _result = cmd.add_element("result")
        _result.set_attribute("id", result_id)

        _assigned = cmd.add_element("assigned_to")
        _user = _assigned.add_element("user")
        _user.set_attribute("id", assigned_to_user_id)

        _note = cmd.add_element("open_note", note)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def delete_ticket(
        self, ticket_id: str, *, ultimate: Optional[bool] = False
    ):
        """Deletes an existing ticket

        Arguments:
            ticket_id: UUID of the ticket to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.delete_ticket.__name__, argument='ticket_id'
            )

        cmd = XmlCommand("delete_ticket")
        cmd.set_attribute("ticket_id", ticket_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def get_tickets(
        self,
        *,
        trash: Optional[bool] = None,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
    ) -> Any:
        """Request a list of tickets

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: True to request the tickets in the trashcan

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tickets")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_ticket(self, ticket_id: str) -> Any:
        """Request a single ticket

        Arguments:
            ticket_id: UUID of an existing ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.get_ticket.__name__, argument='ticket_id'
            )

        cmd = XmlCommand("get_tickets")
        cmd.set_attribute("ticket_id", ticket_id)
        return self._send_xml_command(cmd)

    def get_vulnerabilities(
        self, *, filter: Optional[str] = None, filter_id: Optional[str] = None
    ) -> Any:
        """Request a list of vulnerabilities

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_vulns")

        add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_vulnerability(self, vulnerability_id: str) -> Any:
        """Request a single vulnerability

        Arguments:
            vulnerability_id: ID of an existing vulnerability

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not vulnerability_id:
            raise RequiredArgument(
                function=self.get_vulnerability.__name__,
                argument='vulnerability_id',
            )

        cmd = XmlCommand("get_vulns")
        cmd.set_attribute("vuln_id", vulnerability_id)
        return self._send_xml_command(cmd)

    def modify_ticket(
        self,
        ticket_id: str,
        *,
        status: Optional[TicketStatus] = None,
        note: Optional[str] = None,
        assigned_to_user_id: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Modify a single ticket

        Arguments:
            ticket_id: UUID of an existing ticket
            status: New status for the ticket
            note: Note for the status change. Required if status is set.
            assigned_to_user_id: UUID of the user the ticket should be assigned
                to
            comment: Comment for the ticket

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not ticket_id:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument='ticket_id'
            )

        if status and not note:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument='note'
            )

        if note and not status:
            raise RequiredArgument(
                function=self.modify_ticket.__name__, argument='status'
            )

        cmd = XmlCommand("modify_ticket")
        cmd.set_attribute("ticket_id", ticket_id)

        if assigned_to_user_id:
            _assigned = cmd.add_element("assigned_to")
            _user = _assigned.add_element("user")
            _user.set_attribute("id", assigned_to_user_id)

        if status:
            if not isinstance(status, self.types.TicketStatus):
                raise InvalidArgumentType(
                    function=self.modify_ticket.__name__,
                    argument='status',
                    arg_type=TicketStatus.__name__,
                )

            cmd.add_element('status', status.value)
            cmd.add_element('{}_note'.format(status.name.lower()), note)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def create_filter(
        self,
        name: str,
        *,
        filter_type: Optional[FilterType] = None,
        comment: Optional[str] = None,
        term: Optional[str] = None,
    ) -> Any:
        """Create a new filter

        Arguments:
            name: Name of the new filter
            filter_type: Filter for entity type
            comment: Comment for the filter
            term: Filter term e.g. 'name=foo'

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_filter.__name__, argument="name"
            )

        cmd = XmlCommand("create_filter")
        _xmlname = cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            if not isinstance(filter_type, self.types.FilterType):
                raise InvalidArgumentType(
                    function=self.create_filter.__name__,
                    argument="filter_type",
                    arg_type=self.types.FilterType.__name__,
                )

            cmd.add_element("type", filter_type.value)

        return self._send_xml_command(cmd)

    def modify_filter(
        self,
        filter_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        term: Optional[str] = None,
        filter_type: Optional[FilterType] = None,
    ) -> Any:
        """Modifies an existing filter.

        Arguments:
            filter_id: UUID of the filter to be modified
            comment: Comment on filter.
            name: Name of filter.
            term: Filter term.
            filter_type: Resource type filter applies to.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.modify_filter.__name__, argument='filter_id'
            )

        cmd = XmlCommand("modify_filter")
        cmd.set_attribute("filter_id", filter_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if term:
            cmd.add_element("term", term)

        if filter_type:
            if not isinstance(filter_type, self.types.FilterType):
                raise InvalidArgumentType(
                    function=self.modify_filter.__name__,
                    argument='filter_type',
                    arg_type=FilterType.__name__,
                )
            cmd.add_element("type", filter_type.value)

        return self._send_xml_command(cmd)

    def create_schedule(
        self,
        name: str,
        icalendar: str,
        timezone: str,
        *,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new schedule based in `iCalendar`_ data.

        Example:
            Requires https://pypi.org/project/icalendar/

            .. code-block:: python

                import pytz

                from datetime import datetime

                from icalendar import Calendar, Event

                cal = Calendar()

                cal.add('prodid', '-//Foo Bar//')
                cal.add('version', '2.0')

                event = Event()
                event.add('dtstamp', datetime.now(tz=pytz.UTC))
                event.add('dtstart', datetime(2020, 1, 1, tzinfo=pytz.utc))

                cal.add_component(event)

                gmp.create_schedule(
                    name="My Schedule",
                    icalendar=cal.to_ical(),
                    timezone='UTC'
                )


        Arguments:
            name: Name of the new schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalender events e.g
                Europe/Berlin. If the datetime values in the icalendar data are
                missing timezone information this timezone gets applied.
                Otherwise the datetime values from the icalendar data are
                displayed in this timezone
            comment: Comment on schedule.

        Returns:
            The response. See :py:meth:`send_command` for details.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
        if not name:
            raise RequiredArgument(
                function=self.create_schedule.__name__, argument='name'
            )
        if not icalendar:
            raise RequiredArgument(
                function=self.create_schedule.__name__, argument='icalendar'
            )
        if not timezone:
            raise RequiredArgument(
                function=self.create_schedule.__name__, argument='timezone'
            )

        cmd = XmlCommand("create_schedule")

        cmd.add_element("name", name)
        cmd.add_element("icalendar", icalendar)
        cmd.add_element("timezone", timezone)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def modify_schedule(
        self,
        schedule_id: str,
        *,
        name: Optional[str] = None,
        icalendar: Optional[str] = None,
        timezone: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Modifies an existing schedule

        Arguments:
            schedule_id: UUID of the schedule to be modified
            name: Name of the schedule
            icalendar: `iCalendar`_ (RFC 5545) based data.
            timezone: Timezone to use for the icalender events e.g
                Europe/Berlin. If the datetime values in the icalendar data are
                missing timezone information this timezone gets applied.
                Otherwise the datetime values from the icalendar data are
                displayed in this timezone
            commenhedule.

        Returns:
            The response. See :py:meth:`send_command` for details.

        .. _iCalendar:
            https://tools.ietf.org/html/rfc5545
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.modify_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("modify_schedule")
        cmd.set_attribute("schedule_id", schedule_id)

        if name:
            cmd.add_element("name", name)

        if icalendar:
            cmd.add_element("icalendar", icalendar)

        if timezone:
            cmd.add_element("timezone", timezone)

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_credential(self, credential_id: str) -> Any:
        """Clone an existing credential

        Arguments:
            credential_id: UUID of an existing credential to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.clone_credential.__name__,
                argument='credential_id',
            )

        cmd = XmlCommand("create_credential")
        cmd.add_element("copy", credential_id)
        return self._send_xml_command(cmd)

    def clone_filter(self, filter_id: str) -> Any:
        """Clone an existing filter

        Arguments:
            filter_id: UUID of an existing filter to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.clone_filter.__name__, argument='filter_id'
            )

        cmd = XmlCommand("create_filter")
        cmd.add_element("copy", filter_id)
        return self._send_xml_command(cmd)

    def create_group(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        special: Optional[bool] = False,
        users: Optional[List[str]] = None,
    ) -> Any:
        """Create a new group

        Arguments:
            name: Name of the new group
            comment: Comment for the group
            special: Create permission giving members full access to each
                other's entities
            users: List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_group.__name__, argument='name'
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if special:
            _xmlspecial = cmd.add_element("specials")
            _xmlspecial.add_element("full")

        if users:
            cmd.add_element("users", to_comma_list(users))

        return self._send_xml_command(cmd)

    def clone_group(self, group_id: str) -> Any:
        """Clone an existing group

        Arguments:
            group_id: UUID of an existing group to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.clone_group.__name__, argument='group_id'
            )

        cmd = XmlCommand("create_group")
        cmd.add_element("copy", group_id)
        return self._send_xml_command(cmd)

    def clone_permission(self, permission_id: str) -> Any:
        """Clone an existing permission

        Arguments:
            permission_id: UUID of an existing permission to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.clone_permission.__name__,
                argument='permission_id',
            )

        cmd = XmlCommand("create_permission")
        cmd.add_element("copy", permission_id)
        return self._send_xml_command(cmd)

    def clone_report_format(
        self, report_format_id: [Union[str, ReportFormatType]]
    ) -> Any:
        """Clone a report format from an existing one

        Arguments:
            report_format_id: UUID of the existing report format
                              or ReportFormatType (enum)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.clone_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("create_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.add_element("copy", report_format_id)
        return self._send_xml_command(cmd)

    def import_report_format(self, report_format: str) -> Any:
        """Import a report format from XML

        Arguments:
            report_format: Report format XML as string to import. This XML must
                contain a :code:`<get_report_formats_response>` root element.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format:
            raise RequiredArgument(
                function=self.import_report_format.__name__,
                argument='report_format',
            )

        cmd = XmlCommand("create_report_format")

        try:
            cmd.append_xml_str(report_format)
        except etree.XMLSyntaxError as e:
            raise InvalidArgument(
                function=self.import_report_format.__name__,
                argument='report_format',
            ) from e

        return self._send_xml_command(cmd)

    def create_role(
        self,
        name: str,
        *,
        comment: Optional[str] = None,
        users: Optional[List[str]] = None,
    ) -> Any:
        """Create a new role

        Arguments:
            name: Name of the role
            comment: Comment for the role
            users: List of user names to add to the role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """

        if not name:
            raise RequiredArgument(
                function=self.create_role.__name__, argument='name'
            )

        cmd = XmlCommand("create_role")
        cmd.add_element("name", name)

        if comment:
            cmd.add_element("comment", comment)

        if users:
            cmd.add_element("users", to_comma_list(users))

        return self._send_xml_command(cmd)

    def clone_role(self, role_id: str) -> Any:
        """Clone an existing role

        Arguments:
            role_id: UUID of an existing role to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.clone_role.__name__, argument='role_id'
            )

        cmd = XmlCommand("create_role")
        cmd.add_element("copy", role_id)
        return self._send_xml_command(cmd)

    def create_scanner(
        self,
        name: str,
        host: str,
        port: int,
        scanner_type: ScannerType,
        credential_id: str,
        *,
        ca_pub: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Any:
        """Create a new scanner

        Arguments:
            name: Name of the scanner
            host: The host of the scanner
            port: The port of the scanner
            scanner_type: Type of the scanner.
            credential_id: UUID of client certificate credential for the
                scanner
            ca_pub: Certificate of CA to verify scanner certificate
            comment: Comment for the scanner
        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='name'
            )

        if not host:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='host'
            )

        if not port:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='port'
            )

        if not scanner_type:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='scanner_type'
            )

        if not credential_id:
            raise RequiredArgument(
                function=self.create_scanner.__name__, argument='credential_id'
            )

        if not isinstance(scanner_type, self.types.ScannerType):
            raise InvalidArgumentType(
                function=self.create_scanner.__name__,
                argument='scanner_type',
                arg_type=self.types.ScannerType.__name__,
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("name", name)
        cmd.add_element("host", host)
        cmd.add_element("port", str(port))
        cmd.add_element("type", scanner_type.value)

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        cmd.add_element("credential", attrs={"id": str(credential_id)})

        if comment:
            cmd.add_element("comment", comment)

        return self._send_xml_command(cmd)

    def clone_scanner(self, scanner_id: str) -> Any:
        """Clone an existing scanner

        Arguments:
            scanner_id: UUID of an existing scanner to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.clone_scanner.__name__, argument='scanner_id'
            )

        cmd = XmlCommand("create_scanner")
        cmd.add_element("copy", scanner_id)
        return self._send_xml_command(cmd)

    def clone_schedule(self, schedule_id: str) -> Any:
        """Clone an existing schedule

        Arguments:
            schedule_id: UUID of an existing schedule to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.clone_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("create_schedule")
        cmd.add_element("copy", schedule_id)
        return self._send_xml_command(cmd)

    def clone_tag(self, tag_id: str) -> Any:
        """Clone an existing tag

        Arguments:
            tag_id: UUID of an existing tag to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.clone_tag.__name__, argument='tag_id'
            )

        cmd = XmlCommand("create_tag")
        cmd.add_element("copy", tag_id)
        return self._send_xml_command(cmd)

    def create_user(
        self,
        name: str,
        *,
        password: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Optional[List[str]] = None,
        ifaces_allow: Optional[bool] = False,
        role_ids: Optional[List[str]] = None,
    ) -> Any:
        """Create a new user

        Arguments:
            name: Name of the user
            password: Password of the user
            hosts: A list of host addresses (IPs, DNS names)
            hosts_allow: If True allow only access to passed hosts otherwise
                deny access. Default is False for deny hosts.
            ifaces: A list of interface names
            ifaces_allow: If True allow only access to passed interfaces
                otherwise deny access. Default is False for deny interfaces.
            role_ids: A list of role UUIDs for the user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not name:
            raise RequiredArgument(
                function=self.create_user.__name__, argument='name'
            )

        cmd = XmlCommand("create_user")
        cmd.add_element("name", name)

        if password:
            cmd.add_element("password", password)

        if hosts:
            cmd.add_element(
                "hosts",
                to_comma_list(hosts),
                attrs={"allow": to_bool(hosts_allow)},
            )

        if ifaces:
            cmd.add_element(
                "ifaces",
                to_comma_list(ifaces),
                attrs={"allow": to_bool(ifaces_allow)},
            )

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        return self._send_xml_command(cmd)

    def clone_user(self, user_id: str) -> Any:
        """Clone an existing user

        Arguments:
            user_id: UUID of existing user to clone from

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id:
            raise RequiredArgument(
                function=self.clone_user.__name__, argument='user_id'
            )

        cmd = XmlCommand("create_user")
        cmd.add_element("copy", user_id)
        return self._send_xml_command(cmd)

    def delete_credential(
        self, credential_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing credential

        Arguments:
            credential_id: UUID of the credential to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.delete_credential.__name__,
                argument='credential_id',
            )

        cmd = XmlCommand("delete_credential")
        cmd.set_attribute("credential_id", credential_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_filter(
        self, filter_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing filter

        Arguments:
            filter_id: UUID of the filter to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not filter_id:
            raise RequiredArgument(
                function=self.delete_filter.__name__, argument='filter_id'
            )

        cmd = XmlCommand("delete_filter")
        cmd.set_attribute("filter_id", filter_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_group(
        self, group_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing group

        Arguments:
            group_id: UUID of the group to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.delete_group.__name__, argument='group_id'
            )

        cmd = XmlCommand("delete_group")
        cmd.set_attribute("group_id", group_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_permission(
        self, permission_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing permission

        Arguments:
            permission_id: UUID of the permission to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not permission_id:
            raise RequiredArgument(
                function=self.delete_permission.__name__,
                argument='permission_id',
            )

        cmd = XmlCommand("delete_permission")
        cmd.set_attribute("permission_id", permission_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_report_format(
        self,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        *,
        ultimate: Optional[bool] = False,
    ) -> Any:
        """Deletes an existing report format

        Arguments:
            report_format_id: UUID of the report format to be deleted.
                              or ReportFormatType (enum)
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.delete_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("delete_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_role(
        self, role_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing role

        Arguments:
            role_id: UUID of the role to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.delete_role.__name__, argument='role_id'
            )

        cmd = XmlCommand("delete_role")
        cmd.set_attribute("role_id", role_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_scanner(
        self, scanner_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing scanner

        Arguments:
            scanner_id: UUID of the scanner to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.delete_scanner.__name__, argument='scanner_id'
            )

        cmd = XmlCommand("delete_scanner")
        cmd.set_attribute("scanner_id", scanner_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_schedule(
        self, schedule_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing schedule

        Arguments:
            schedule_id: UUID of the schedule to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not schedule_id:
            raise RequiredArgument(
                function=self.delete_schedule.__name__, argument='schedule_id'
            )

        cmd = XmlCommand("delete_schedule")
        cmd.set_attribute("schedule_id", schedule_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_tag(
        self, tag_id: str, *, ultimate: Optional[bool] = False
    ) -> Any:
        """Deletes an existing tag

        Arguments:
            tag_id: UUID of the tag to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
        if not tag_id:
            raise RequiredArgument(
                function=self.delete_tag.__name__, argument='tag_id'
            )

        cmd = XmlCommand("delete_tag")
        cmd.set_attribute("tag_id", tag_id)
        cmd.set_attribute("ultimate", to_bool(ultimate))

        return self._send_xml_command(cmd)

    def delete_user(
        self,
        user_id: str = None,
        *,
        name: Optional[str] = None,
        inheritor_id: Optional[str] = None,
        inheritor_name: Optional[str] = None,
    ) -> Any:
        """Deletes an existing user

        Either user_id or name must be passed.

        Arguments:
            user_id: UUID of the task to be deleted.
            name: The name of the user to be deleted.
            inheritor_id: The ID of the inheriting user or "self". Overrides
                inheritor_name.
            inheritor_name: The name of the inheriting user.

        """
        if not user_id and not name:
            raise RequiredArgument(
                function=self.delete_user.__name__, argument='user_id or name'
            )

        cmd = XmlCommand("delete_user")

        if user_id:
            cmd.set_attribute("user_id", user_id)

        if name:
            cmd.set_attribute("name", name)

        if inheritor_id:
            cmd.set_attribute("inheritor_id", inheritor_id)
        if inheritor_name:
            cmd.set_attribute("inheritor_name", inheritor_name)

        return self._send_xml_command(cmd)

    def describe_auth(self) -> Any:
        """Describe authentication methods

        Returns a list of all used authentication methods if such a list is
        available.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("describe_auth"))

    def empty_trashcan(self) -> Any:
        """Empty the trashcan

        Remove all entities from the trashcan. **Attention:** this command can
        not be reverted

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("empty_trashcan"))

    def get_credentials(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        scanners: Optional[bool] = None,
        trash: Optional[bool] = None,
        targets: Optional[bool] = None,
    ) -> Any:
        """Request a list of credentials

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            scanners: Whether to include a list of scanners using the
                credentials
            trash: Whether to get the trashcan credentials instead
            targets: Whether to include a list of targets using the credentials

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_credentials")

        add_filter(cmd, filter, filter_id)

        if scanners is not None:
            cmd.set_attribute("scanners", to_bool(scanners))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if targets is not None:
            cmd.set_attribute("targets", to_bool(targets))

        return self._send_xml_command(cmd)

    def get_credential(
        self,
        credential_id: str,
        *,
        scanners: Optional[bool] = None,
        targets: Optional[bool] = None,
        credential_format: Optional[CredentialFormat] = None,
    ) -> Any:
        """Request a single credential

        Arguments:
            credential_id: UUID of an existing credential
            scanners: Whether to include a list of scanners using the
                credentials
            targets: Whether to include a list of targets using the credentials
            credential_format: One of "key", "rpm", "deb", "exe" or "pem"

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not credential_id:
            raise RequiredArgument(
                function=self.get_credential.__name__, argument='credential_id'
            )

        cmd = XmlCommand("get_credentials")
        cmd.set_attribute("credential_id", credential_id)

        if credential_format:
            if not isinstance(credential_format, CredentialFormat):
                raise InvalidArgumentType(
                    function=self.get_credential.__name__,
                    argument='credential_format',
                    arg_type=CredentialFormat.__name__,
                )

            cmd.set_attribute("format", credential_format.value)

        if scanners is not None:
            cmd.set_attribute("scanners", to_bool(scanners))

        if targets is not None:
            cmd.set_attribute("targets", to_bool(targets))

        return self._send_xml_command(cmd)

    def get_feeds(self) -> Any:
        """Request the list of feeds

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_feeds"))

    def get_filters(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
    ) -> Any:
        """Request a list of filters

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan filters instead
            alerts: Whether to include list of alerts that use the filter.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_filters")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        return self._send_xml_command(cmd)

    def get_filter(
        self, filter_id: str, *, alerts: Optional[bool] = None
    ) -> Any:
        """Request a single filter

        Arguments:
            filter_id: UUID of an existing filter
            alerts: Whether to include list of alerts that use the filter.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_filters")

        if not filter_id:
            raise RequiredArgument(
                function=self.get_filter.__name__, argument='filter_id'
            )

        cmd.set_attribute("filter_id", filter_id)

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        return self._send_xml_command(cmd)

    def get_groups(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
    ) -> Any:
        """Request a list of groups

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan groups instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_groups")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_group(self, group_id: str) -> Any:
        """Request a single group

        Arguments:
            group_id: UUID of an existing group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_groups")

        if not group_id:
            raise RequiredArgument(
                function=self.get_group.__name__, argument='group_id'
            )

        cmd.set_attribute("group_id", group_id)
        return self._send_xml_command(cmd)

    def get_permissions(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
    ) -> Any:
        """Request a list of permissions

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get permissions in the trashcan instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_permissions")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_permission(self, permission_id: str) -> Any:
        """Request a single permission

        Arguments:
            permission_id: UUID of an existing permission

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_permissions")

        if not permission_id:
            raise RequiredArgument(
                function=self.get_permission.__name__, argument='permission_id'
            )

        cmd.set_attribute("permission_id", permission_id)
        return self._send_xml_command(cmd)

    def get_preferences(
        self, *, nvt_oid: Optional[str] = None, config_id: Optional[str] = None
    ) -> Any:
        """Request a list of preferences

        When the command includes a config_id attribute, the preference element
        includes the preference name, type and value, and the NVT to which the
        preference applies. Otherwise, the preference element includes just the
        name and value, with the NVT and type built into the name.

        Arguments:
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_preferences")

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        if config_id:
            cmd.set_attribute("config_id", config_id)

        return self._send_xml_command(cmd)

    def get_preference(
        self,
        name: str,
        *,
        nvt_oid: Optional[str] = None,
        config_id: Optional[str] = None,
    ) -> Any:
        """Request a nvt preference

        Arguments:
            name: name of a particular preference
            nvt_oid: OID of nvt
            config_id: UUID of scan config of which to show preference values

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_preferences")

        if not name:
            raise RequiredArgument(
                function=self.get_preference.__name__, argument='name'
            )

        cmd.set_attribute("preference", name)

        if nvt_oid:
            cmd.set_attribute("nvt_oid", nvt_oid)

        if config_id:
            cmd.set_attribute("config_id", config_id)

        return self._send_xml_command(cmd)

    def get_report_formats(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        alerts: Optional[bool] = None,
        params: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of report formats

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan report formats instead
            alerts: Whether to include alerts that use the report format
            params: Whether to include report format parameters
            details: Include report format file, signature and parameters

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_report_formats")

        add_filter(cmd, filter, filter_id)

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        if alerts is not None:
            cmd.set_attribute("alerts", to_bool(alerts))

        if params is not None:
            cmd.set_attribute("params", to_bool(params))

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_report_format(
        self, report_format_id: Union[str, ReportFormatType]
    ) -> Any:
        """Request a single report format

        Arguments:
            report_format_id: UUID of an existing report format
                              or ReportFormatType (enum)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_report_formats")

        if not report_format_id:
            raise RequiredArgument(
                function=self.get_report_format.__name__,
                argument='report_format_id',
            )

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_roles(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
    ) -> Any:
        """Request a list of roles

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan roles instead

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_roles")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        return self._send_xml_command(cmd)

    def get_role(self, role_id: str) -> Any:
        """Request a single role

        Arguments:
            role_id: UUID of an existing role

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.get_role.__name__, argument='role_id'
            )

        cmd = XmlCommand("get_roles")
        cmd.set_attribute("role_id", role_id)
        return self._send_xml_command(cmd)

    def get_scanners(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        details: Optional[bool] = None,
    ) -> Any:
        """Request a list of scanners

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scanners instead
            details:  Whether to include extra details like tasks using this
                scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_scanners")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if details is not None:
            cmd.set_attribute("details", to_bool(details))

        return self._send_xml_command(cmd)

    def get_scanner(self, scanner_id: str) -> Any:
        """Request a single scanner

        Arguments:
            scanner_id: UUID of an existing scanner

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_scanners")

        if not scanner_id:
            raise RequiredArgument(
                function=self.get_scanner.__name__, argument='scanner_id'
            )

        cmd.set_attribute("scanner_id", scanner_id)

        # for single entity always request all details
        cmd.set_attribute("details", "1")
        return self._send_xml_command(cmd)

    def get_schedules(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        tasks: Optional[bool] = None,
    ) -> Any:
        """Request a list of schedules

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan schedules instead
            tasks: Whether to include tasks using the schedules

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_schedules")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_schedule(
        self, schedule_id: str, *, tasks: Optional[bool] = None
    ) -> Any:
        """Request a single schedule

        Arguments:
            schedule_id: UUID of an existing schedule
            tasks: Whether to include tasks using the schedules

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_schedules")

        if not schedule_id:
            raise RequiredArgument(
                function=self.get_schedule.__name__, argument='schedule_id'
            )

        cmd.set_attribute("schedule_id", schedule_id)

        if tasks is not None:
            cmd.set_attribute("tasks", to_bool(tasks))

        return self._send_xml_command(cmd)

    def get_settings(self, *, filter: Optional[str] = None) -> Any:
        """Request a list of user settings

        Arguments:
            filter: Filter term to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_settings")

        if filter:
            cmd.set_attribute("filter", filter)

        return self._send_xml_command(cmd)

    def get_setting(self, setting_id: str) -> Any:
        """Request a single setting

        Arguments:
            setting_id: UUID of an existing setting

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_settings")

        if not setting_id:
            raise RequiredArgument(
                function=self.get_setting.__name__, argument='setting_id'
            )

        cmd.set_attribute("setting_id", setting_id)
        return self._send_xml_command(cmd)

    def get_system_reports(
        self,
        *,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        brief: Optional[bool] = None,
        slave_id: Optional[str] = None,
    ) -> Any:
        """Request a list of system reports

        Arguments:
            name: A string describing the required system report
            duration: The number of seconds into the past that the system report
                should include
            start_time: The start of the time interval the system report should
                include in ISO time format
            end_time: The end of the time interval the system report should
                include in ISO time format
            brief: Whether to include the actual system reports
            slave_id: UUID of GMP scanner from which to get the system reports

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_system_reports")

        if name:
            cmd.set_attribute("name", name)

        if duration is not None:
            if not isinstance(duration, Integral):
                raise InvalidArgument("duration needs to be an integer number")

            cmd.set_attribute("duration", str(duration))

        if start_time:
            cmd.set_attribute("start_time", str(start_time))

        if end_time:
            cmd.set_attribute("end_time", str(end_time))

        if brief is not None:
            cmd.set_attribute("brief", to_bool(brief))

        if slave_id:
            cmd.set_attribute("slave_id", slave_id)

        return self._send_xml_command(cmd)

    def get_tags(
        self,
        *,
        filter: Optional[str] = None,
        filter_id: Optional[str] = None,
        trash: Optional[bool] = None,
        names_only: Optional[bool] = None,
    ) -> Any:
        """Request a list of tags

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get tags from the trashcan instead
            names_only: Whether to get only distinct tag names

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tags")

        add_filter(cmd, filter, filter_id)

        if trash is not None:
            cmd.set_attribute("trash", to_bool(trash))

        if names_only is not None:
            cmd.set_attribute("names_only", to_bool(names_only))

        return self._send_xml_command(cmd)

    def get_tag(self, tag_id: str) -> Any:
        """Request a single tag

        Arguments:
            tag_id: UUID of an existing tag

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_tags")

        if not tag_id:
            raise RequiredArgument(
                function=self.get_tag.__name__, argument='tag_id'
            )

        cmd.set_attribute("tag_id", tag_id)
        return self._send_xml_command(cmd)

    def get_users(
        self, *, filter: Optional[str] = None, filter_id: Optional[str] = None
    ) -> Any:
        """Request a list of users

        Arguments:
            filter: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_users")

        add_filter(cmd, filter, filter_id)

        return self._send_xml_command(cmd)

    def get_user(self, user_id: str) -> Any:
        """Request a single user

        Arguments:
            user_id: UUID of an existing user

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("get_users")

        if not user_id:
            raise RequiredArgument(
                function=self.get_user.__name__, argument='user_id'
            )

        cmd.set_attribute("user_id", user_id)
        return self._send_xml_command(cmd)

    def get_version(self) -> Any:
        """Get the Greenbone Manager Protocol version used by the remote gvmd

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("get_version"))

    def help(
        self, *, format: Optional[str] = None, help_type: Optional[str] = ""
    ) -> Any:
        """Get the help text

        Arguments:
            format: One of "html", "rnc", "text" or "xml
            help_type: One of "brief" or "". Default ""

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        cmd = XmlCommand("help")

        if help_type not in ("", "brief"):
            raise InvalidArgument(
                'help_type argument must be an empty string or "brief"'
            )

        cmd.set_attribute("type", help_type)

        if format:
            if not format.lower() in ("html", "rnc", "text", "xml"):
                raise InvalidArgument(
                    "help format Argument must be one of html, rnc, text or "
                    "xml"
                )

            cmd.set_attribute("format", format)

        return self._send_xml_command(cmd)

    def modify_auth(self, group_name: str, auth_conf_settings: dict) -> Any:
        """Modifies an existing auth.

        Arguments:
            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_name:
            raise RequiredArgument(
                function=self.modify_auth.__name__, argument='group_name'
            )
        if not auth_conf_settings:
            raise RequiredArgument(
                function=self.modify_auth.__name__,
                argument='auth_conf_settings',
            )
        cmd = XmlCommand("modify_auth")
        _xmlgroup = cmd.add_element("group", attrs={"name": str(group_name)})

        for key, value in auth_conf_settings.items():
            _xmlauthconf = _xmlgroup.add_element("auth_conf_setting")
            _xmlauthconf.add_element("key", key)
            _xmlauthconf.add_element("value", value)

        return self._send_xml_command(cmd)

    def modify_group(
        self,
        group_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing group.

        Arguments:
            group_id: UUID of group to modify.
            comment: Comment on group.
            name: Name of group.
            users: List of user names to be in the group

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not group_id:
            raise RequiredArgument(
                function=self.modify_group.__name__, argument='group_id'
            )

        cmd = XmlCommand("modify_group")
        cmd.set_attribute("group_id", group_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if users:
            cmd.add_element("users", to_comma_list(users))

        return self._send_xml_command(cmd)

    def modify_report_format(
        self,
        report_format_id: Optional[Union[str, ReportFormatType]] = None,
        *,
        active: Optional[bool] = None,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        param_name: Optional[str] = None,
        param_value: Optional[str] = None,
    ) -> Any:
        """Modifies an existing report format.

        Arguments:
            report_format_id: UUID of report format to modify
                              or ReportFormatType (enum)
            active: Whether the report format is active.
            name: The name of the report format.
            summary: A summary of the report format.
            param_name: The name of the param.
            param_value: The value of the param.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.modify_report_format.__name__,
                argument='report_format_id ',
            )

        cmd = XmlCommand("modify_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        if active is not None:
            cmd.add_element("active", to_bool(active))

        if name:
            cmd.add_element("name", name)

        if summary:
            cmd.add_element("summary", summary)

        if param_name:
            _xmlparam = cmd.add_element("param")
            _xmlparam.add_element("name", param_name)

            if param_value is not None:
                _xmlparam.add_element("value", param_value)

        return self._send_xml_command(cmd)

    def modify_role(
        self,
        role_id: str,
        *,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        users: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing role.

        Arguments:
            role_id: UUID of role to modify.
            comment: Name of role.
            name: Comment on role.
            users: List of user names.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not role_id:
            raise RequiredArgument(
                function=self.modify_role.__name__, argument='role_id argument'
            )

        cmd = XmlCommand("modify_role")
        cmd.set_attribute("role_id", role_id)

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if users:
            cmd.add_element("users", to_comma_list(users))

        return self._send_xml_command(cmd)

    def modify_scanner(
        self,
        scanner_id: str,
        *,
        scanner_type: Optional[ScannerType] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        comment: Optional[str] = None,
        name: Optional[str] = None,
        ca_pub: Optional[str] = None,
        credential_id: Optional[str] = None,
    ) -> Any:
        """Modifies an existing scanner.

        Arguments:
            scanner_id: UUID of scanner to modify.
            scanner_type: New type of the Scanner.
            host: Host of the scanner.
            port: Port of the scanner.
            comment: Comment on scanner.
            name: Name of scanner.
            ca_pub: Certificate of CA to verify scanner's certificate.
            credential_id: UUID of the client certificate credential for the
                Scanner.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.modify_scanner.__name__,
                argument='scanner_id argument',
            )

        cmd = XmlCommand("modify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        if scanner_type is not None:
            if not isinstance(scanner_type, self.types.ScannerType):
                raise InvalidArgumentType(
                    function=self.modify_scanner.__name__,
                    argument='scanner_type',
                    arg_type=self.types.ScannerType.__name__,
                )

            cmd.add_element("type", scanner_type.value)

        if host:
            cmd.add_element("host", host)

        if port:
            cmd.add_element("port", str(port))

        if comment:
            cmd.add_element("comment", comment)

        if name:
            cmd.add_element("name", name)

        if ca_pub:
            cmd.add_element("ca_pub", ca_pub)

        if credential_id:
            cmd.add_element("credential", attrs={"id": str(credential_id)})

        return self._send_xml_command(cmd)

    def modify_setting(
        self,
        setting_id: Optional[str] = None,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ) -> Any:
        """Modifies an existing setting.

        Arguments:
            setting_id: UUID of the setting to be changed.
            name: The name of the setting. Either setting_id or name must be
                passed.
            value: The value of the setting.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not setting_id and not name:
            raise RequiredArgument(
                function=self.modify_setting.__name__,
                argument='setting_id or name argument',
            )

        if value is None:
            raise RequiredArgument(
                function=self.modify_setting.__name__, argument='value argument'
            )

        cmd = XmlCommand("modify_setting")

        if setting_id:
            cmd.set_attribute("setting_id", setting_id)
        else:
            cmd.add_element("name", name)

        cmd.add_element("value", to_base64(value))

        return self._send_xml_command(cmd)

    def modify_user(
        self,
        user_id: str = None,
        name: str = None,
        *,
        new_name: Optional[str] = None,
        comment: Optional[str] = None,
        password: Optional[str] = None,
        auth_source: Optional[UserAuthType] = None,
        role_ids: Optional[List[str]] = None,
        hosts: Optional[List[str]] = None,
        hosts_allow: Optional[bool] = False,
        ifaces: Optional[List[str]] = None,
        ifaces_allow: Optional[bool] = False,
        group_ids: Optional[List[str]] = None,
    ) -> Any:
        """Modifies an existing user. Most of the fields need to be supplied
        for changing a single field even if no change is wanted for those.
        Else empty values are inserted for the missing fields instead.
        Arguments:
            user_id: UUID of the user to be modified. Overrides name element
                argument.
            name: The name of the user to be modified. Either user_id or name
                must be passed.
            new_name: The new name for the user.
            comment: Comment on the user.
            password: The password for the user.
            auth_source: Source allowed for authentication for this user.
            roles_id: List of roles UUIDs for the user.
            hosts: User access rules: List of hosts.
            hosts_allow: Defines how the hosts list is to be interpreted.
                If False (default) the list is treated as a deny list.
                All hosts are allowed by default except those provided by
                the hosts parameter. If True the list is treated as a
                allow list. All hosts are denied by default except those
                provided by the hosts parameter.
            ifaces: User access rules: List of ifaces.
            ifaces_allow: Defines how the ifaces list is to be interpreted.
                If False (default) the list is treated as a deny list.
                All ifaces are allowed by default except those provided by
                the ifaces parameter. If True the list is treated as a
                allow list. All ifaces are denied by default except those
                provided by the ifaces parameter.
            group_ids: List of group UUIDs for the user.

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not user_id and not name:
            raise RequiredArgument(
                function=self.modify_user.__name__, argument='user_id or name'
            )

        cmd = XmlCommand("modify_user")

        if user_id:
            cmd.set_attribute("user_id", user_id)
        else:
            cmd.add_element("name", name)

        if new_name:
            cmd.add_element("new_name", new_name)

        if role_ids:
            for role in role_ids:
                cmd.add_element("role", attrs={"id": role})

        if hosts:
            cmd.add_element(
                "hosts",
                to_comma_list(hosts),
                attrs={"allow": to_bool(hosts_allow)},
            )

        if ifaces:
            cmd.add_element(
                "ifaces",
                to_comma_list(ifaces),
                attrs={"allow": to_bool(ifaces_allow)},
            )

        if comment:
            cmd.add_element("comment", comment)

        if password:
            cmd.add_element("password", password)

        if auth_source:
            _xmlauthsrc = cmd.add_element("sources")
            _xmlauthsrc.add_element("source", auth_source.value)

        if group_ids:
            _xmlgroups = cmd.add_element("groups")
            for group_id in group_ids:
                _xmlgroups.add_element("group", attrs={"id": group_id})

        return self._send_xml_command(cmd)

    def restore(self, entity_id: str) -> Any:
        """Restore an entity from the trashcan

        Arguments:
            entity_id: ID of the entity to be restored from the trashcan

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not entity_id:
            raise RequiredArgument(
                function=self.restore.__name__, argument='entity_id'
            )

        cmd = XmlCommand("restore")
        cmd.set_attribute("id", entity_id)

        return self._send_xml_command(cmd)

    def sync_cert(self) -> Any:
        """Request a synchronization with the CERT feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_cert"))

    def sync_feed(self) -> Any:
        """Request a synchronization with the NVT feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_feed"))

    def sync_scap(self) -> Any:
        """Request a synchronization with the SCAP feed service

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        return self._send_xml_command(XmlCommand("sync_scap"))

    def verify_report_format(
        self, report_format_id: Union[str, ReportFormatType]
    ) -> Any:
        """Verify an existing report format

        Verifies the trust level of an existing report format. It will be
        checked whether the signature of the report format currently matches the
        report format. This includes the script and files used to generate
        reports of this format. It is *not* verified if the report format works
        as expected by the user.

        Arguments:
            report_format_id: UUID of the report format to be verified
                              or ReportFormatType (enum)

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not report_format_id:
            raise RequiredArgument(
                function=self.verify_report_format.__name__,
                argument='report_format_id',
            )

        cmd = XmlCommand("verify_report_format")

        if isinstance(report_format_id, ReportFormatType):
            report_format_id = report_format_id.value

        cmd.set_attribute("report_format_id", report_format_id)

        return self._send_xml_command(cmd)

    def verify_scanner(self, scanner_id: str) -> Any:
        """Verify an existing scanner

        Verifies if it is possible to connect to an existing scanner. It is
        *not* verified if the scanner works as expected by the user.

        Arguments:
            scanner_id: UUID of the scanner to be verified

        Returns:
            The response. See :py:meth:`send_command` for details.
        """
        if not scanner_id:
            raise RequiredArgument(
                function=self.verify_scanner.__name__, argument='scanner_id'
            )

        cmd = XmlCommand("verify_scanner")
        cmd.set_attribute("scanner_id", scanner_id)

        return self._send_xml_command(cmd)
