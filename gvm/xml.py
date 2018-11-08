# -*- coding: utf-8 -*-
# Copyright (C) 2018 Greenbone Networks GmbH
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

import defusedxml.lxml as secET

from lxml import etree

class XmlCommandElement:

    def __init__(self, element):
        self._element = element

    def add_element(self, name, text=None, attrs=None):
        node = etree.SubElement(self._element, name, attrib=attrs)
        node.text = text
        return XmlCommandElement(node)

    def set_attribute(self, name, value):
        self._element.set(name, value)

    def set_attributes(self, attrs):
        """Set several attributes at once.

        Arguments:
            attrs (dict): Attributes to be set on the element
        """
        for key, value in attrs.items():
            self._element.set(key, value)

    def append_xml_str(self, xml_text):
        """Append a xml element in string format."""
        node = secET.fromstring(xml_text)
        self._element.append(node)

    def to_string(self):
        return etree.tostring(self._element).decode('utf-8')

    def __str__(self):
        return self.to_string()


class XmlCommand(XmlCommandElement):

    def __init__(self, name):
        super().__init__(etree.Element(name))


class _GmpCommandFactory:

    """Factory to create gmp - Greenbone Management Protocol - commands
    """


    def modify_target_command(self, target_id, kwargs):
        """Generates xml string for modify target on gvmd."""
        if not target_id:
            raise ValueError('modify_target requires a target_id element')

        cmd = XmlCommand('modify_target')
        cmd.set_attribute('target_id', target_id)

        comment = kwargs.get('comment', '')
        if comment:
            cmd.add_element('comment', comment)

        name = kwargs.get('name', '')
        if name:
            cmd.add_element('name', name)

        hosts = kwargs.get('hosts', '')
        if hosts:
            cmd.add_element('hosts', hosts)

        copy = kwargs.get('copy', '')
        if copy:
            cmd.add_element('copy', copy)

        exclude_hosts = kwargs.get('exclude_hosts', '')
        if exclude_hosts:
            cmd.add_element('exclude_hosts', exclude_hosts)

        alive_tests = kwargs.get('alive_tests', '')
        if alive_tests:
            cmd.add_element('alive_tests', alive_tests)

        reverse_lookup_only = kwargs.get('reverse_lookup_only', '')
        if reverse_lookup_only:
            cmd.add_element('reverse_lookup_only', reverse_lookup_only)

        reverse_lookup_unify = kwargs.get('reverse_lookup_unify', '')
        if reverse_lookup_unify:
            cmd.add_element('reverse_lookup_unify', reverse_lookup_unify)

        port_range = kwargs.get('port_range', '')
        if port_range:
            cmd.add_element('port_range', port_range)

        port_list = kwargs.get('port_list', '')
        if port_list:
            cmd.add_element('port_list', attrs={'id': str(port_list)})

        return cmd.to_string()

    def modify_task_command(self, task_id, kwargs):
        """Generates xml string for modify task on gvmd."""
        if not task_id:
            raise ValueError('modify_task requires a task_id element')

        cmd = XmlCommand('modify_task')
        cmd.set_attribute('task_id', task_id)

        name = kwargs.get('name', '')
        if name:
            cmd.add_element('name', name)

        comment = kwargs.get('comment', '')
        if comment:
            cmd.add_element('comment', comment)

        target_id = kwargs.get('target_id', '')
        if target_id:
            cmd.add_element('target', attrs={'id': target_id})

        scanner = kwargs.get('scanner', '')
        if scanner:
            cmd.add_element('scanner', attrs={'id': scanner})

        schedule_periods = kwargs.get('schedule_periods', '')
        if schedule_periods:
            cmd.add_element('schedule_periods', str(schedule_periods))

        schedule = kwargs.get('schedule', '')
        if schedule:
            cmd.add_element('schedule', attrs={'id': str(schedule)})

        alert = kwargs.get('alert', '')
        if alert:
            cmd.add_element('alert', attrs={'id': str(alert)})

        observers = kwargs.get('observers', '')
        if observers:
            cmd.add_element('observers', str(observers))

        preferences = kwargs.get('preferences', '')
        if preferences:
            _xmlprefs = cmd.add_element('preferences')
            for n in range(len(preferences["scanner_name"])):
                preferences_scanner_name = preferences["scanner_name"][n]
                preferences_value = preferences["value"][n]
                _xmlpref = _xmlprefs.add_element('preference')
                _xmlpref.add_element('scanner_name', preferences_scanner_name)
                _xmlpref.add_element('value', preferences_value)

        file = kwargs.get('file', '')
        if file:
            file_name = file['name']
            file_action = file['action']
            if file_action != "update" and file_action != "remove":
                raise ValueError('action can only be "update" or "remove"!')
            cmd.add_element('file', attrs={'name': file_name,
                                           'action': file_action})

        return cmd.to_string()

    def modify_user_command(self, kwargs):
        """Generates xml string for modify user on gvmd."""
        user_id = kwargs.get('user_id', '')
        name = kwargs.get('name', '')

        if not user_id and not name:
            raise ValueError('modify_user requires '
                             'either a user_id or a name element')

        cmd = XmlCommand('modify_user')
        cmd.set_attribute('user_id', str(user_id))

        new_name = kwargs.get('new_name', '')
        if new_name:
            cmd.add_element('new_name', new_name)

        password = kwargs.get('password', '')
        if password:
            cmd.add_element('password', password)

        role_ids = kwargs.get('role_ids', '')
        if len(role_ids) > 0:
            for role in role_ids:
                cmd.add_element('role', attrs={'id': str(role)})

        hosts = kwargs.get('hosts', '')
        hosts_allow = kwargs.get('hosts_allow', '')
        if hosts or hosts_allow:
            cmd.add_element('hosts', hosts, attrs={'allow': str(hosts_allow)})

        ifaces = kwargs.get('ifaces', '')
        ifaces_allow = kwargs.get('ifaces_allow', '')
        if ifaces or ifaces_allow:
            cmd.add_element('ifaces', ifaces,
                            attrs={'allow': str(ifaces_allow)})

        sources = kwargs.get('sources', '')
        if sources:
            cmd.add_element('sources', sources)

        return cmd.to_string()

    def delete_agent_command(self, kwargs):
        """Generates xml string for delete agent on gvmd"""
        cmd = XmlCommand('delete_agent')
        for key, value in kwargs.items():
            cmd.set_attribute(key, value)

        return cmd.to_string()

    def delete_alert_command(self, kwargs):
        """Generates xml string for delete alert on gvmd"""
        cmd = XmlCommand('delete_alert')
        for key, value in kwargs.items():
            cmd.set_attribute(key, value)

        return cmd.to_string()

    def delete_asset_command(self, asset_id, ultimate=0):
        """Generates xml string for delete asset on gvmd"""
        cmd = XmlCommand('delete_asset')
        cmd.set_attribute('asset_id', asset_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_config_command(self, config_id, ultimate=0):
        """Generates xml string for delete config on gvmd"""
        cmd = XmlCommand('delete_config')
        cmd.set_attribute('config_id', config_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_credential_command(self, credential_id, ultimate=0):
        """Generates xml string for delete credential on gvmd"""
        cmd = XmlCommand('delete_credential')
        cmd.set_attribute('credential_id', credential_id)
        cmd.set_attribute('ultimate', ultimate)
        return cmd.to_string()

    def delete_filter_command(self, filter_id, ultimate=0):
        """Generates xml string for delete filter on gvmd"""
        cmd = XmlCommand('delete_filter')
        cmd.set_attribute('filter_id', filter_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_group_command(self, group_id, ultimate=0):
        """Generates xml string for delete group on gvmd"""
        cmd = XmlCommand('delete_group')
        cmd.set_attribute('group_id', group_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_note_command(self, note_id, ultimate=0):
        """Generates xml string for delete note on gvmd"""
        cmd = XmlCommand('delete_note')
        cmd.set_attribute('note_id', note_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_override_command(self, override_id, ultimate=0):
        """Generates xml string for delete override on gvmd"""
        cmd = XmlCommand('delete_override')
        cmd.set_attribute('override_id', override_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_permission_command(self, permission_id, ultimate=0):
        """Generates xml string for delete permission on gvmd"""
        cmd = XmlCommand('delete_permission')
        cmd.set_attribute('permission_id', permission_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_port_list_command(self, port_list_id, ultimate=0):
        """Generates xml string for delete port on gvmd"""
        cmd = XmlCommand('delete_port_list')
        cmd.set_attribute('port_list_id', port_list_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_port_range_command(self, port_range_id):
        """Generates xml string for delete port on gvmd"""
        cmd = XmlCommand('delete_port_range')
        cmd.set_attribute('port_range_id', port_range_id)

        return cmd.to_string()

    def delete_report_command(self, report_id):
        """Generates xml string for delete report on gvmd"""
        cmd = XmlCommand('delete_report')
        cmd.set_attribute('report_id', report_id)

        return cmd.to_string()

    def delete_report_format_command(self, report_format_id, ultimate=0):
        """Generates xml string for delete report on gvmd"""
        cmd = XmlCommand('delete_report_format')
        cmd.set_attribute('report_format_id', report_format_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_role_command(self, role_id, ultimate=0):
        """Generates xml string for delete role on gvmd"""
        cmd = XmlCommand('delete_role')
        cmd.set_attribute('role_id', role_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_scanner_command(self, scanner_id, ultimate=0):
        """Generates xml string for delete scanner on gvmd"""
        cmd = XmlCommand('delete_scanner')
        cmd.set_attribute('scanner_id', scanner_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_schedule_command(self, schedule_id, ultimate=0):
        """Generates xml string for delete schedule on gvmd"""
        # if self.ask_yes_or_no('Are you sure to delete this schedule? '):
        cmd = XmlCommand('delete_schedule')
        cmd.set_attribute('schedule_id', schedule_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_tag_command(self, tag_id, ultimate=0):
        """Generates xml string for delete tag on gvmd"""
        cmd = XmlCommand('delete_tag')
        cmd.set_attribute('tag_id', tag_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_target_command(self, target_id, ultimate=0):
        """Generates xml string for delete target on gvmd"""
        cmd = XmlCommand('delete_target')
        cmd.set_attribute('target_id', target_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_task_command(self, task_id, ultimate=0):
        """Generates xml string for delete task on gvmd"""
        cmd = XmlCommand('delete_task')
        cmd.set_attribute('task_id', task_id)
        cmd.set_attribute('ultimate', ultimate)

        return cmd.to_string()

    def delete_user_command(self, kwargs):
        """Generates xml string for delete user on gvmd"""
        cmd = XmlCommand('delete_user')

        user_id = kwargs.get('user_id', '')
        if user_id:
            cmd.set_attribute('user_id', user_id)

        name = kwargs.get('name', '')
        if name:
            cmd.set_attribute('name', name)

        inheritor_id = kwargs.get('inheritor_id', '')
        if inheritor_id:
            cmd.set_attribute('inheritor_id', inheritor_id)

        inheritor_name = kwargs.get('inheritor_name', '')
        if inheritor_name:
            cmd.set_attribute('inheritor_name', inheritor_name)

        return cmd.to_string()

    def get_assets_command(self, kwargs):
        """Generates xml string for get assets on gvmd."""
        cmd = XmlCommand('get_assets')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_credentials_command(self, kwargs):
        """Generates xml string for get credentials on gvmd."""
        cmd = XmlCommand('get_credentials')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_configs_command(self, kwargs):
        """Generates xml string for get configs on gvmd."""
        cmd = XmlCommand('get_configs')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_feeds_command(self, kwargs):
        """Generates xml string for get feeds on gvmd."""
        cmd = XmlCommand('get_feeds')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_filters_command(self, kwargs):
        """Generates xml string for get filters on gvmd."""
        cmd = XmlCommand('get_filters')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_groups_command(self, kwargs):
        """Generates xml string for get groups on gvmd."""
        cmd = XmlCommand('get_groups')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_info_command(self, kwargs):
        """Generates xml string for get info on gvmd."""
        cmd = XmlCommand('get_info')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_notes_command(self, kwargs):
        """Generates xml string for get notes on gvmd."""
        cmd = XmlCommand('get_notes')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_nvts_command(self, kwargs):
        """Generates xml string for get nvts on gvmd."""
        cmd = XmlCommand('get_nvts')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_nvt_families_command(self, kwargs):
        """Generates xml string for get nvt on gvmd."""
        cmd = XmlCommand('get_nvt_families')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_overrides_command(self, kwargs):
        """Generates xml string for get overrides on gvmd."""
        cmd = XmlCommand('get_overrides')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_permissions_command(self, kwargs):
        """Generates xml string for get permissions on gvmd."""
        cmd = XmlCommand('get_permissions')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_port_lists_command(self, kwargs):
        """Generates xml string for get port on gvmd."""
        cmd = XmlCommand('get_port_lists')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_preferences_command(self, kwargs):
        """Generates xml string for get preferences on gvmd."""
        cmd = XmlCommand('get_preferences')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_reports_command(self, kwargs):
        """Generates xml string for get reports on gvmd."""
        cmd = XmlCommand('get_reports')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_report_formats_command(self, kwargs):
        """Generates xml string for get report on gvmd."""
        cmd = XmlCommand('get_report_formats')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_results_command(self, kwargs):
        """Generates xml string for get results on gvmd."""
        cmd = XmlCommand('get_results')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_roles_command(self, kwargs):
        """Generates xml string for get roles on gvmd."""
        cmd = XmlCommand('get_roles')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_scanners_command(self, kwargs):
        """Generates xml string for get scanners on gvmd."""
        cmd = XmlCommand('get_scanners')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_schedules_command(self, kwargs):
        """Generates xml string for get schedules on gvmd."""
        cmd = XmlCommand('get_schedules')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_settings_command(self, kwargs):
        """Generates xml string for get settings on gvmd."""
        cmd = XmlCommand('get_settings')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_system_reports_command(self, kwargs):
        """Generates xml string for get system on gvmd."""
        cmd = XmlCommand('get_system')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_tags_command(self, kwargs):
        """Generates xml string for get tags on gvmd."""
        cmd = XmlCommand('get_tags')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_targets_command(self, kwargs):
        """Generates xml string for get targets on gvmd."""
        cmd = XmlCommand('get_targets')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_tasks_command(self, kwargs):
        """Generates xml string for get tasks on gvmd."""
        cmd = XmlCommand('get_tasks')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def get_users_command(self, kwargs):
        """Generates xml string for get users on gvmd."""
        cmd = XmlCommand('get_users')
        cmd.set_attributes(kwargs)
        return cmd.to_string()

    def move_task_command(self, task_id, slave_id):
        """Generates xml string for move task on gvmd."""
        cmd = XmlCommand('move_task')
        cmd.set_attribute('task_id', task_id)
        cmd.set_attribute('slave_id', slave_id)
        return cmd.to_string()

    def restore_command(self, entity_id):
        """Generates xml string for restore on gvmd."""
        cmd = XmlCommand('restore')
        cmd.set_attribute('id', entity_id)
        return cmd.to_string()

    def resume_task_command(self, task_id):
        """Generates xml string for resume task on gvmd."""
        cmd = XmlCommand('resume_task')
        cmd.set_attribute('task_id', task_id)
        return cmd.to_string()

    def start_task_command(self, task_id):
        """Generates xml string for start task on gvmd."""
        cmd = XmlCommand('start_task')
        cmd.set_attribute('task_id', task_id)
        return cmd.to_string()

    def stop_task_command(self, task_id):
        """Generates xml string for stop task on gvmd."""
        cmd = XmlCommand('stop_task')
        cmd.set_attribute('task_id', task_id)
        return cmd.to_string()

    def test_alert_command(self, alert_id):
        """Generates xml string for test alert on gvmd."""
        cmd = XmlCommand('test_alert')
        cmd.set_attribute('alert_id', alert_id)
        return cmd.to_string()

    def verify_agent_command(self, agent_id):
        """Generates xml string for verify agent on gvmd."""
        cmd = XmlCommand('verify_agent')
        cmd.set_attribute('agent_id', agent_id)
        return cmd.to_string()

    def verify_report_format_command(self, report_format_id):
        """Generates xml string for verify report format on gvmd."""
        cmd = XmlCommand('verify_report_format')
        cmd.set_attribute('report_format_id', report_format_id)
        return cmd.to_string()

    def verify_scanner_command(self, scanner_id):
        """Generates xml string for verify scanner on gvmd."""
        cmd = XmlCommand('verify_scanner')
        cmd.set_attribute('scanner_id', scanner_id)
        return cmd.to_string()


def pretty_print(xml):
    """Prints beautiful XML-Code

    This function gets an object of list<lxml.etree._Element>
    or directly a lxml element.
    Print it with good readable format.

    Arguments:
        xml: List<lxml.etree.Element> or directly a lxml element
    """
    if isinstance(xml, list):
        for item in xml:
            if etree.iselement(item):
                print(etree.tostring(item, pretty_print=True).decode('utf-8'))
            else:
                print(item)
    elif etree.iselement(xml):
        print(etree.tostring(xml, pretty_print=True).decode('utf-8'))
