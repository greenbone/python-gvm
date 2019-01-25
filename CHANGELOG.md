# python-gvm 1.0.0 (unreleased)

## gvm.protocols.gmpv7

* Aligned ALIVE_TESTS declaration with gsa list
* Refactor `modify_task` to use same arguments as `create_task`
* Added preferences argument to `create_task` method
* Allow to pass either user_id or name to `delete_user`
* Don't require inheritor_id or inheritor_name for `delete_user`
* Added validation of alive_tests argument to `create_target` method
* Removed hosts_ordering argument from `modify_target`
* Added ssh_credential_port argument to `modify_target`
* Fixed sending resource id in `modify_tag`
* Don't require ca_pub for `create_scanner`
* Change port argument for `create_scanner` to be an integer
* Refactor `modify_scanner` method: Adjust argument types corresponding to
 `create_scanner` and only require scanner_id
* Require either setting_id or name for `modify_setting` not both arguments
* Allow empty string a value argument for `modify_setting`
* Require either user_id or name for `modify_user` not both arguments
* Removed sources argument from `modify_user` method
* Removed `modify_report` method
* Removed unused comment argument from `create_note` and `create_override`
* Updated argument types for `create_note`, `create_override`, `modify_note`
  and `modify_override`
* The arguments threat (and new_threat) for `create_note`, `modify_note`,
  `create_override` and `modify_override` must be one of 'High', 'Medium',
  'Low', 'Alarm', 'Log' or 'Debug' now
* `modify_config` is marked as deprecated and will be removed in future. One of
  the more specific `modify_config_set_` method should be used instead.
* Fixed generating XML for `get_nvts` command
* Fixed generating XML for `get_settings` command
* Fixed generating XML for `get_credentials` command
* Renamed create_asset method to create_host and dropped asset_type parameter.
  It is only possible to create host assets.
* Updated and improved validation of `create_schedule` and
  `modify_schedule` arguments
* Removed the format parameter from `get_credentials` method
* Removed the task_id and nvt_oid parameters from `get_notes` and
  `get_overrides` methods
* Split getting a single preference by name from `get_preferences` method into
  `get_preference`
* Fixed wrong order of key and value for condition_data, event_data and
  method_data dict parameters of `modify_alert` method.

# python-gvm 1.0.0.beta2 (04.12.2018)

## gvm.protocols.base

* Fix: Don't close the connection after each send/read command sequence
  automatically. This fixes sending more then one privileged gmp command after
  authentication.

## gvm.protocols.gmpv7

* Fixed generating XML for help command
* **help** method **type** argument got renamed to **help_type**
* **help** method **help_type** argument will be checked for invalid values
* Fixed wrong order of key and value for condition_data, event_data and
  method_data dict parameters of **create_alert** method.
* **create_credential** requires a credential_type argument now.
* Optional parameters are required to be passed as keyword arguments.
* Fixed **get_reports** sending the wrong protocol command
* Removed **format_id** argument from get_reports
* **get_report** method **format_id** argument got renamed to
  **report_format_id**
* Removed **alert_id** argument from **get_reports**
* Added new **trigger_alert** method for triggering an alert method on a
  specific report.
* Fixed **create_permission** method
* Check if scanner_type is one of '1' (OSP Scanner) or '2' (OpenVAS Scanner) in
  **create_scanner** method.
* Fixed **get_config** sending the correct protocol command.
* Added **import_config** method to import a scan config from xml.

## gvm.xml

* Added helper function to validate xml input **gvm.xml.validate_xml_string**
* **pretty_print** accepts a xml string as input too

## gvm.connections

* Optional arguments for connection class constructors must be passed as
  keyword arguments.
* Add **finish_send** method to connections. The method allows to indicate to
  the server sending data is finished and no additional data has to be received.
* Don't crash if huge content is returned in a xml response. This fixes e.g.
  **get_reports** for bigger report data.
* It's possible to wait indefinitely by deactivating the timeouts via passing
  None as timeout argument to the connection class constructors now.
* Removed unused **read_timeout** argument from **UnixSocketConnection**

# python-gvm 1.0.0.beta1 (13.11.2018)

python-gvm was a part of [gvm-tools](https://github.com/greenbone/gvm-tools)
prior version 2.0. It got extracted from gvm-tools and completely overhauled.

Some notable changes are:

* The package name changed from *gmp* to *gvm*.
* The type of connection is passed to a more generic Gmp class instead of
  having to select the connection when creating the gmp object.
* Support for different protocols and versions has been added. Currently
  supported protocols are OSP v1 and GMP v7.
* Full API documentation is available at https://python-gvm.readthedocs.io/en/latest/.
* Possible arguments to protocol methods are documented.
* Arguments should be passed as keywords

## Gmp API changes

* **create_report** has been renamed to **import_report**.
* Requesting single entities has been extracted from the list commands e.g.
  **get_task(task_id)** instead of **get_tasks(task_id=task_id)**.
* **get_info** requests a single info entity.
* **get_info_list** requests a list of info entities.
* **filt_id** argument is called **filter_id** at all Gmp methods.
* **report_filter** argument for **get_reports** got renamed to **filter**.
  **report_filt_id** is **filter_id** now.
* **create_schedule** **start_time** and **end_time** arguments got split into
  several parameters.
* Plural arguments like **hosts**, **users**, ... always require a list now.
* **create_alert** **event**, **condition** and **method** arguments got
  revised and split.
* boolean parameters expect True and False and not 1, 0, '1' or '0' now.
* **get_assets** type parameter got renamed to **asset_type**
* Copying an entity via the **copy** argument has been removed and extracted to
  own **clone** methods e.g. **clone_task**.
