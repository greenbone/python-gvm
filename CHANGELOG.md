# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org)html).

## [Unreleased]

**Dropped support for GMP v7, v8 and v9!**

### Added
* Introduced new explicit API calls for SecInfo: `get_nvt()`, `get_nvt_list()`, `get_cpe()`, `get_cpe_list()`, `get_cve()`, `get_cve_list()`, `get_cert_bund_advisory()`, `get_cert_bund_advisory_list()`, `get_dnf_cert_advisory()`, `get_dnf_cert_advisory_list()`, `get_oval_definition()`, `get_oval_definition_list()`. [#456](https://github.com/greenbone/python-gvm/pull/456)

### Changed
* Detached the Tags API calls from the GMP class into a new `TagsMixin`. [#468](https://github.com/greenbone/python-gvm/pull/468)
* Detached the Feeds API calls from the GMP class into a new `FeedsMixin`. [#468](https://github.com/greenbone/python-gvm/pull/468)
* Detached the Aggregates API calls from the GMP class into a new `AggregatesMixin`. [#468](https://github.com/greenbone/python-gvm/pull/468)
* Detached the EntityType from the GMP types class into a new `entites` file. [#467](https://github.com/greenbone/python-gvm/pull/467)
* Detached the Users API calls from the GMP class into a new `UsersMixin`. [#467](https://github.com/greenbone/python-gvm/pull/467)
* Detached the Permissions API calls from the GMP class into a new `PermissionsMixin`. [#467](https://github.com/greenbone/python-gvm/pull/467)
* Detached the Scanner API calls from the GMP class into a new `ScannersMixin`. [#466](https://github.com/greenbone/python-gvm/pull/466)
* Detached the Credential API calls from the GMP class into a new `CredentialsMixin`. [#466](https://github.com/greenbone/python-gvm/pull/466)
* Changed all API calls for `_config` to `_scan_config` to match other Greenbone components. [#465](https://github.com/greenbone/python-gvm/pull/465)
* Detached Config and Policy calls from GMP class into new `ScanConfigsMixin` and `PoliciesMixin`. [#465](https://github.com/greenbone/python-gvm/pull/465)
* Detached the Audit API calls from the GMP class into a new `AuditsMixin`. [#464](https://github.com/greenbone/python-gvm/pull/464)
* Split up `get_asset(s)` into `get_host(s)` and `get_operating_system(s)`. [#459](https://github.com/greenbone/python-gvm/pull/459)
* Split up `delete_asset` into `delete_host` and `delete_operating_system`. [#459](https://github.com/greenbone/python-gvm/pull/459)
* Split up `modify_asset` into `modify_host` and `modify_operating_system`. [#459](https://github.com/greenbone/python-gvm/pull/459)
* Deleted `AssetType`. It is not required anymore. [#459](https://github.com/greenbone/python-gvm/pull/458)
* Detach TLS-Certificates and assets into `TLSCertificatesMixin`, `HostsMixin` and `OperatingSystemsMixin`. [#459](https://github.com/greenbone/python-gvm/pull/458)
* Detached the Alerts API calls from the GMP class into a new `AlertsMixin`. [#458](https://github.com/greenbone/python-gvm/pull/458)
* Detached the Notes and Overrides API calls from the GMP class into a new `NotesMixin` and `OverridesMixin`. [#457](https://github.com/greenbone/python-gvm/pull/457)
* Changed the API calls `get_nvt()` and `get_nvts()` to `get_scan_config_nvt()` and `get_scan_config_nvts()`.  [#456](https://github.com/greenbone/python-gvm/pull/456)
* Detached the `InfoType` from the GMP types class.  [#456](https://github.com/greenbone/python-gvm/pull/456)
* Detached the SecInfo (CPE, CVE, NVT, CERT-BUND, DNF-CERT, OVAL Definitions) calls from GMP class into new `SecInfoMixin`. [#456](https://github.com/greenbone/python-gvm/pull/456)
* Detached the PortList and PortRange API calls from the GMP class into a new `PortListMixin`. [#446](https://github.com/greenbone/python-gvm/pull/446)
* Detached the Target API calls from the GMP class into a new `TargetsMixin`. [#446](https://github.com/greenbone/python-gvm/pull/446)
* Detached the `AliveTest` from the GMP types class. [#446](https://github.com/greenbone/python-gvm/pull/446)
* Detached the `PortListType` from the GMP types class. [#446](https://github.com/greenbone/python-gvm/pull/446)
* Detached the ReportFormatType from the GMP types class. [#445](https://github.com/greenbone/python-gvm/pull/445)
* Detached the Report API calls from the GMP class into a new `ReportMixin`. [#445](https://github.com/greenbone/python-gvm/pull/445)
* Detached the Task API calls from the GMP class into a new `TasksMixin`. [#443](https://github.com/greenbone/python-gvm/pull/443)
* Moved helper functions from gmp to utils. The response XML will not be recovered by the parser anymore! [#442](https://github.com/greenbone/python-gvm/pull/442)

### Deprecated
### Removed
* Removed `TimeUnit`. It was used for schedules before iCal and is not required anymore.
* Removed `Gmpv214Mixin`. [#467](https://github.com/greenbone/python-gvm/pull/467)
* Remove support of delete host/operating system by a report . [#459](https://github.com/greenbone/python-gvm/pull/459)
* Remove deprecated `make_unique` parameter from `Targets`. [#446](https://github.com/greenbone/python-gvm/pull/446)
* Removed deprecated `Agents` completely. [#441](https://github.com/greenbone/python-gvm/pull/441)
* **Dropped support** for GMP v7, v8 and v9! The oldest usable GMP version is 20.8 
  [#436](https://github.com/greenbone/python-gvm/pull/436)
  [#437](https://github.com/greenbone/python-gvm/pull/437)
  [#438](https://github.com/greenbone/python-gvm/pull/438)
  [#439](https://github.com/greenbone/python-gvm/pull/439)
  [#444](https://github.com/greenbone/python-gvm/pull/444)

### Fixed

[Unreleased]: https://github.com/greenbone/python-gvm/compare/v21.4.0...HEAD


## [21.4.0] - 2021-04-26
### Changed
* `get_feed` can also be requested with `GVMD_DATA` for 20.08 and newer, added `GVMD_DATA` to the FeedType and updated API call [#434](https://github.com/greenbone/python-gvm/pull/434)

[21.4.0]: https://github.com/greenbone/python-gvm/compare/v21.1.3...v21.4.0

## [21.1.3] - 2021-01-27
### Added
* Added protocol version "next" and GMP 21.04 doc [#384](https://github.com/greenbone/python-gvm/pull/384)

### Fixed
* Add missing ReportFormatType to GMP 21.04 [#385](https://github.com/greenbone/python-gvm/pull/385)

[21.1.3]: https://github.com/greenbone/python-gvm/compare/v21.1.2...v21.1.3

## [21.1.2] - 2021-01-27
### Added
* Added allow_simultaneous_ips param for targets [#380](https://github.com/greenbone/python-gvm/pull/380)

### Removed
* dropped the GMP Scanner (4) from `ScannerTypes` for v21.4 [#383](https://github.com/greenbone/python-gvm/pull/383)

### Fixed
* removing `timeout` from `get_nvt()` [#376](https://github.com/greenbone/python-gvm/pull/376)
* Add `ReportFormatType` and `get_report_format_id_from_string` to `latest.py`, so it is usable with `import gvm.protcols.latest`[#381](https://github.com/greenbone/python-gvm/pull/381)
* Fixing `import_report()` for v9 and v20.8 and newer, removed the `task_name` and `task_comment` parameters, that do not work anymore [#377](https://github.com/greenbone/python-gvm/pull/377)

[21.1.2]: https://github.com/greenbone/python-gvm/compare/v21.1.1...v21.1.2

## [21.1.1] - 2021-01-05
### Fixed
* Fixed release issues, through rerelease.

[21.1.1]: https://github.com/greenbone/python-gvm/compare/v21.1.0...v21.1.1

## [21.1.0] - 2021-01-05
### Added
* CI tests Python 3.9 now. [#367](https://github.com/greenbone/python-gvm/pull/367)

### Deprecated
* Dropped Python 3.5 and Python 3.6 support. Python 3.7+ is required now. [#367](https://github.com/greenbone/python-gvm/pull/367)

### Fixed
* Add missing types and functions to "latest" GMP [#369](https://github.com/greenbone/python-gvm/pull/369)

[21.1.0]: https://github.com/greenbone/python-gvm/compare/v20.12.1...v21.1.0

## [20.12.1] - 2020-12-16
### Added
* Added AUDIT and POLICY to EntityType enum [#353](https://github.com/greenbone/python-gvm/pull/353)

### Changed
* Support "all" argument in modify_scan_config_set_family_selection [#368](https://github.com/greenbone/python-gvm/pull/368)
* added the `audits` parameter to `get_policy` [#345](https://github.com/greenbone/python-gvm/pull/345)
* Update get_aggregates params in GMP 9.0 and newer [#359](https://github.com/greenbone/python-gvm/pull/359)

### Fixed
* added `get_info_list` to v20.08, so it works as expected with new `InfoType` [#362](https://github.com/greenbone/python-gvm/pull/362)

[20.12.1]: https://github.com/greenbone/python-gvm/compare/v20.11.3...v20.12.1

## [20.11.3] - 2020-11-26
### Added
* Adding parameters to `get_nvt command`, so it requests all details [#348](https://github.com/greenbone/python-gvm/pull/348)
* Improved the `modify_user` function for gmpv7 and gmpv214. Added ability to change comment, groups and authentication method of user. Meaning of name parameter got changed for gmpv214 only. It is not intended for identifying a user anymore but for specifying the new name of the user [#347](https://github.com/greenbone/python-gvm/pull/347)
* Adding `resume_audit`, `start_audit`, `stop_audit` to gmpv9 [#349](https://github.com/greenbone/python-gvm/pull/349)

### Changed
* Implement tuple for `family` argument for `modify_config_set_family_selection` [#354](https://github.com/greenbone/python-gvm/pull/354)

[20.11.3]: https://github.com/greenbone/python-gvm/compare/v20.11.2...HEAD

## [20.11.2] - 2020-11-17
### Added
* Added the `delete_tls_certificate` function  [#335](https://github.com/greenbone/python-gvm/pull/335)
[20.11.2]: https://github.com/greenbone/python-gvm/compare/v20.11.1...HEAD

## [20.11.1] - 2020-11-16
### Added
* Added the `modify_audit` function [#332](https://github.com/greenbone/python-gvm/pull/332)
* Added the `modify_policy_set_nvt_preference` function [#332](https://github.com/greenbone/python-gvm/pull/332)
* Added the `modify_policy_set_name` function [#332](https://github.com/greenbone/python-gvm/pull/332)
* Added the `modify_policy_set_comment` function [#332](https://github.com/greenbone/python-gvm/pull/332)
* Added the `modify_policy_set_scanner_preference` function [#332](https://github.com/greenbone/python-gvm/pull/332)
* Added the `modify_policy_set_nvt_selection` function [#332](https://github.com/greenbone/python-gvm/pull/332)
* Added the `modify_policy_set_family_selection` function [#332](https://github.com/greenbone/python-gvm/pull/332)

### Changed
* Moved tests for `SeverityLevel` Enum and `get_severity_level_from_string()` [#327](https://github.com/greenbone/python-gvm/pull/327)
* In `get_report()` the `details` parameter is `True` on default now. [#333](https://github.com/greenbone/python-gvm/pull/333)

[20.11.1]: https://github.com/greenbone/python-gvm/compare/v20.11.0...HEAD

## [20.11.0] - 2020-11-03
### Added
* Added `clone_report_format()` and `import_report_format()` [#309](https://github.com/greenbone/python-gvm/pull/309)
* Added the `get_x_from_string()` functions to `latest` [#308](https://github.com/greenbone/python-gvm/pull/308)
* Added the `ReportFormatType` that can be used instead of a report_format_id [#311](https://github.com/greenbone/python-gvm/pull/311)
* Added tests for constructor of SSHConnection, TLSConnection, UnixSocketConnection and GvmConnection [#321](https://github.com/greenbone/python-gvm/pull/321)

### Fixed
* Corrected `seconds_active` parameter to `days_active` for notes and overrides. [#307](https://github.com/greenbone/python-gvm/pull/307)
* Fixed SSHConnection throws TypeError if port is None [#321](https://github.com/greenbone/python-gvm/pull/321)
* Fixed GvmConnection timeout set to None if None is passed [#321](https://github.com/greenbone/python-gvm/pull/321)
* Fixed TLSConnection values set to None instead of default values when None is passed for these values [#321](https://github.com/greenbone/python-gvm/pull/321)
* Fixed UnixSocketConnection values set to None instead of default when None is passed for these values [#321](https://github.com/greenbone/python-gvm/pull/321)

[20.11.0]: https://github.com/greenbone/python-gvm/compare/v20.9.1...HEAD

## [20.9.1] - 2020-09-25
### Added
* Added `modify_config_set_name`. [#295](https://github.com/greenbone/python-gvm/pull/295)
* Added logic to accept the new AlertEvents `TICKET_RECEIVED`, `ASSIGNED_TICKET_CHANGED` and `OWNED_TICKET_CHANGED` and the new Condition `SEVERITY_CHANGED`. [#297](https://github.com/greenbone/python-gvm/pull/297)
* Added `create_config_from_osp_scanner`. [#298](https://github.com/greenbone/python-gvm/pull/298)
### Changed
* Added the `details` parameter to `get_tls_certificate` and `get_tls_certificates`. [#293](https://github.com/greenbone/python-gvm/pull/293)
* Added the `comment` parameter to `create_config`. [#294](https://github.com/greenbone/python-gvm/pull/294)
### Fixed
* Fix ScannerType check for newer protocols. [#300](https://github.com/greenbone/python-gvm/pull/300)

[20.9.1]: https://github.com/greenbone/python-gvm/compare/v20.9.0...HEAD

## [20.9.0] - 2020-09-17
### Changed
* Added the `tasks` parameter to `get_config()`. [#289](https://github.com/greenbone/python-gvm/pull/289)
* Renamed `no_details` to `details` in `get_reports()` so it is uniform with all the other calls. [#290](https://github.com/greenbone/python-gvm/pull/290)
### Fixed
- Force garbage clean up when disconnect. [#286](https://github.com/greenbone/python-gvm/pull/286)

[20.9.0]: https://github.com/greenbone/python-gvm/compare/v20.8.1...HEAD

## [20.8.1] - 2020-09-01

### Added

* Added `AlertMethods`: Alemba vFire, Tippingpoint SMS [#275](https://github.com/greenbone/python-gvm/pull/275)
* Added `AlertConditions`: Error, SeverityChanged [#275](https://github.com/greenbone/python-gvm/pull/275)
* Added `AlertEvents`: Assigned ticket changed, Owned ticket changed, Ticket received [#275](https://github.com/greenbone/python-gvm/pull/275)

### Changed

* `pretty_print()` has a new argument that can optionally handle a file. The output is redirected to this file. default is `sys.stdout`, as it is for build-in `print()` [#277](https://github.com/greenbone/python-gvm/pull/277)

### Fixed

* `ARP_PING` is now a field of `AliveTypes`, the old `APR_PING` name is still available. [#281](https://github.com/greenbone/python-gvm/pull/281)
* `modify_task` adds `<alert id="0"/>` if alert_ids array is empty. [#285](https://github.com/greenbone/python-gvm/pull/285)

[20.8.1]: https://github.com/greenbone/python-gvm/compare/v20.8.0...HEAD

## [20.8.0] - 2020-08-19

### Added

* Added support for GMP 20.08 [#254](https://github.com/greenbone/python-gvm/pull/254)

### Changed

* Refactored Gmp classes into mixins [#254](https://github.com/greenbone/python-gvm/pull/254)

### Fixed

* Require method and condition arguments for modify_alert with an event [#267](https://github.com/greenbone/python-gvm/pull/267)
* Add SEVERITY_AT_LEAST to get_alert_condition_from_string [#268](https://github.com/greenbone/python-gvm/pull/268)

[20.8.0]: https://github.com/greenbone/python-gvm/compare/v1.6.0...v20.8.0

## [1.6.0] - 2020-06-10

### Added

* Extend AliveTest and ScannerType enums.
  [#235](https://github.com/greenbone/python-gvm/pull/235)

### Fixed

* Fix python-gvm v8/v9 type checks. [#244](https://github.com/greenbone/python-gvm/pull/244)

[1.6.0]: https://github.com/greenbone/python-gvm/compare/v1.5.0...v1.6.0

## [1.5.0] - 2020-05-12

### Added

* Add full support for audits and policies. Add `get_policy`, `get_policies`,
  `clone_policy`, `delete_policy`, `get_audit`, `get_audits`, `clone_audit` and
  `delete_audit` methods to GMPv9 class. Also do not return policies for config
  requests and audits for task requests [#223](https://github.com/greenbone/python-gvm/pull/223)

### Changed

* If it isn't possible to connect to a Unix Domain Socket a GvmError is raised
  now [#207](https://github.com/greenbone/python-gvm/pull/207)

### Removed

* Dropped version handling code from python-gvm and replaced it with using
  pontos.version [#213](https://github.com/greenbone/python-gvm/pull/213)

[1.5.0]: https://github.com/greenbone/python-gvm/compare/v1.4.0...v1.5.0

## [1.4.0]

### Added
* Added an API and CLI utilities for the version handling in python-gvm
  [#198](https://github.com/greenbone/python-gvm/pull/198)

### Changed
* Replaced `pipenv` with `poetry` for dependency management. `poetry install`
  works a bit different then `pipenv install`. It installs dev packages by
  default and also python-gvm in editable mode. This means after running
  `poetry install` gvm will directly be importable in the virtual python
  environment. [#197](https://github.com/greenbone/python-gvm/pull/197)
* Update error classes to always have meaningful `__str__` and `__repr__`
  method. This allows for easier error printing
  [#199](https://github.com/greenbone/python-gvm/pull/199)

[1.4.0]: https://github.com/greenbone/python-gvm/compare/v1.3.0...v1.4.0

## [1.3.0]

### Added
* Added `GvmServerError`, `GvmClientError`, `GvmResponseError` and `InvalidArgumentType` error type classes [#192](https://github.com/greenbone/python-gvm/pull/192)

### Changed
* Refactored the `InvalidArgument` and `RequiredArgument` errors in the gmp classes [#192](https://github.com/greenbone/python-gvm/pull/192)
* Refactored the status response errors in case of a failure in the communication with the server in `transform.py` [#192](https://github.com/greenbone/python-gvm/pull/192)

[1.3.0]: https://github.com/greenbone/python-gvm/compare/v1.2.0...v1.3.0

## [1.2.0]

### Added
* Added DEFAULT_SSH_PORT and DEFAULT_HOSTNAME constants to `gmp.connection` [#185](https://github.com/greenbone/python-gvm/pull/185)
* Added `determine_remote_gmp_version` and `determine_supported_gmp` methods to
  `gmp.protocols.gmp` module [#186](https://github.com/greenbone/python-gvm/pull/186)

### Fixed
* Added a workaround that fixes the `exclude_hosts`-bug in the method `modify_target`.
  See [#187](https://github.com/greenbone/python-gvm/issues/187) for more details [#188](https://github.com/greenbone/python-gvm/pull/188)
* Fixed value of `EntityType.AGENT` enum [#190](https://github.com/greenbone/python-gvm/pull/190)

[1.2.0]: https://github.com/greenbone/python-gvm/compare/v1.1.0...v1.2.0

## [1.1.0] - 2019-11-22

### Added
* Added ignore_pagination and details arguments for get_report [#163](https://github.com/greenbone/python-gvm/pull/163)
* Introduced Gmpv9 for [GMP 9](https://docs.greenbone.net/API/GMP/gmp-9.0.html)
  support [#157](https://github.com/greenbone/python-gvm/pull/157),
  [#165](https://github.com/greenbone/python-gvm/pull/165),
  [#166](https://github.com/greenbone/python-gvm/pull/166)
* Added new `create_audit` method, to create a task with the `usage_type` `audit` [#157](https://github.com/greenbone/python-gvm/pull/157)
* Added new `create_policy` method, to create a config with the `usage_type` `policy` [#157](https://github.com/greenbone/python-gvm/pull/157)
* Added the new methods `create_tls_certificate`, `modify_tls_certificate` and `clone_tls_certificate` to create, modify and copy TLS certificates [#157](https://github.com/greenbone/python-gvm/pull/157)
* Added the new method `get_tls_certificates`, to request TLS certificates from the server [#157](https://github.com/greenbone/python-gvm/pull/157)
* Added the new method `get_tls_certificate`, to request a single TLS certificate
  from the server [#166](https://github.com/greenbone/python-gvm/pull/166)

### Changed
* Use Gmpv9 in gvm.protocols.latest module [#165](https://github.com/greenbone/python-gvm/pull/165)
* Added type `TLS_CERTIFICATE` to `EntityType` and `FilterType` [#157](https://github.com/greenbone/python-gvm/pull/157)
* Changed the `DEFAULT_UNIX_SOCKET_PATH` [#119](https://github.com/greenbone/python-gvm/pull/162)
* ospv1.py: Don't half shutdown the TLS socket. [#180](https://github.com/greenbone/python-gvm/pull/180)

### Deprecated
* Mark make_unique argument of create_target Gmpv8 as deprecated and ignore it.
  It is already ignored by gvmd with GMP 8 [#156](https://github.com/greenbone/python-gvm/pull/156)

[1.1.0]: https://github.com/greenbone/python-gvm/compare/v1.0.0...v1.1.0

## [1.0.0] - 2019-09-18

### Changed
* Return version tuple from get_protocol_version methods [#154](https://github.com/greenbone/python-gvm/pull/154)

### Fixed
* Fixed `create_tag` and `modify_tag` `resource_type` argument to expect an
  EntityType in `Gmp8` [#150](https://github.com/greenbone/python-gvm/pull/150)
* Re-added `SMB` as an allowed `AlertMethod` for SecInfo events
  [#145](https://github.com/greenbone/python-gvm/pull/145)

[1.0.0]: https://github.com/greenbone/python-gvm/compare/v1.0.0.beta3...v1.0.0

## [1.0.0.beta3] - 2019-07-30

### Added
* Added preferences argument to `create_task` method [#89](https://github.com/greenbone/python-gvm/pull/89)
* Added validation of alive_tests argument to `create_target` method [#88](https://github.com/greenbone/python-gvm/pull/88)
* Added ssh_credential_port argument to `modify_target` [#88](https://github.com/greenbone/python-gvm/pull/88)
* Split getting a single preference by name from `get_preferences` method into
  `get_preference` [#85](https://github.com/greenbone/python-gvm/pull/85)
* Added resource_type argument to `get_aggregates` method [#107](https://github.com/greenbone/python-gvm/pull/107)
* Added an explicit `create_container_task` method [#108](https://github.com/greenbone/python-gvm/pull/108)
* Added Gmpv8 version of create_tag with resource_filter parameter and
  plural resource_ids parameter [#115](https://github.com/greenbone/python-gvm/pull/115)
* Added Gmpv8 version of modify_tag with resource_action parameter,
  resource_filter parameter, plural resource_ids parameter [#115](https://github.com/greenbone/python-gvm/pull/115)
* Added no_details argument to `get_reports` method [#129](https://github.com/greenbone/python-gvm/pull/129)
* Added `get_vulnerabilities` method [#132](https://github.com/greenbone/python-gvm/pull/132)
* Added `get_ticket`, `get_tickets`, `create_ticket`, `clone_ticket`, `modify_ticket` and `delete_ticket`
  APIs to GMPv8 [#132](https://github.com/greenbone/python-gvm/pull/132)
* Added filter types for `host`, `operating system`, `ticket` and `vulnerability`
  [#133](https://github.com/greenbone/python-gvm/pull/133)
* Added a `password only` credential type [#133](https://github.com/greenbone/python-gvm/pull/133)
* Added [type hints](https://docs.python.org/3/library/typing.html) for Gmpv8
  [#136](https://github.com/greenbone/python-gvm/pull/136)
* Added dynamic selection of the Gmp class depending on the GMP version supported
  by the remote manager daemon
  [#141](https://github.com/greenbone/python-gvm/pull/141)
* Added all types as types property to the Gmp classes (e.g gmp.types.EntityType.TASK)
  [#143](https://github.com/greenbone/python-gvm/pull/143)

### Changed
* Renamed `create_asset` method to `create_host` and dropped asset_type
  argument. It is only possible to create host assets. [#77](https://github.com/greenbone/python-gvm/pull/77)
* Require either setting_id or name for `modify_setting` not both arguments [#87](https://github.com/greenbone/python-gvm/pull/87)
* Allow empty string as value argument for `modify_setting` [#87](https://github.com/greenbone/python-gvm/pull/87)
* Require either user_id or name for `modify_user` not both arguments [#87](https://github.com/greenbone/python-gvm/pull/87)
* Updated argument types for `create_note`, `create_override`, `modify_note`
  and `modify_override` [#87](https://github.com/greenbone/python-gvm/pull/87)
* The arguments threat (and new_threat) for `create_note`, `modify_note`,
  `create_override` and `modify_override` must be one of 'High', 'Medium',
  'Low', 'Alarm', 'Log' or 'Debug' now [#87](https://github.com/greenbone/python-gvm/pull/87)
* Allow to pass either user_id or name to `delete_user` [#88](https://github.com/greenbone/python-gvm/pull/88)
* Don't require inheritor_id or inheritor_name for `delete_user`
* Don't require ca_pub for `create_scanner` [#88](https://github.com/greenbone/python-gvm/pull/88)
* Change port argument for `create_scanner` to be an integer [#88](https://github.com/greenbone/python-gvm/pull/88)
* Refactor `modify_scanner` method: Adjust argument types corresponding to
 `create_scanner` and only require scanner_id [#88](https://github.com/greenbone/python-gvm/pull/88)
* Updated and improved validation of `create_schedule` and
  `modify_schedule` arguments [#89](https://github.com/greenbone/python-gvm/pull/89)
* Refactor `modify_task` to use same arguments as `create_task` [#89](https://github.com/greenbone/python-gvm/pull/89)
* Aligned ALIVE_TESTS declaration with list from GSA [#93](https://github.com/greenbone/python-gvm/pull/93)
* Address DeprecationWarning regarding `collections` module [#99](https://github.com/greenbone/python-gvm/pull/99)
* Forbid *'0'* as target_id value for  `create_task` method and move creating a
  container task into an own method [#108](https://github.com/greenbone/python-gvm/pull/108)
* Refresh the dependencies specified via the Pipfile.lock file to their latest
  versions [#113](https://github.com/greenbone/python-gvm/pull/113),
  [#131](https://github.com/greenbone/python-gvm/pull/131)
* Make resource_id optional when creating tags (Gmpv7) [#124](https://github.com/greenbone/python-gvm/pull/124)
* Allow creating tags without resource (Gmpv8) [#125](https://github.com/greenbone/python-gvm/pull/125)
* Adapt modify_tag validation to actual implementation (Gmpv8) [#127](https://github.com/greenbone/python-gvm/pull/127)
* Use Gmpv8 as latest Gmp version [#132](https://github.com/greenbone/python-gvm/pull/132)
* Dropped the `make_unique` arguments from `create_filter` and `create_target`
  methods in Gmpv8 [#133](https://github.com/greenbone/python-gvm/pull/133)
* Introduced Enum classes for authentication and privacy algorithms of SNMP
  credentials [#133](https://github.com/greenbone/python-gvm/pull/133)
* Extended `InvalidArgument` and `RequiredArgument` errors to allow passing
  argument and function name as keyword parameter [#134](https://github.com/greenbone/python-gvm/pull/134)
* Renamed `modify_target` and `create_target` argument `alive_tests` to `alive_test`
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use [enum](https://docs.python.org/3/library/enum.html) AliveTests for
  `alive_test` arguments
  [#136](https://github.com/greenbone/python-gvm/pull/136)
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `AlertCondition`, `AlertEvent` and `AlertMethod` enums for `create_alert`
  and `modify_alert` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `AssetType` enum for `get_asset` and `get_assets` method
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `CredentialFormat` enum for `get_credential` method
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `CredentialType` enum for `create_credential` and `modify_credential`
  methods
  [#132](https://github.com/greenbone/python-gvm/pull/132)
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `EntityType` enum for `create_permission`, `create_tag`, `get_aggregates`,
  `modify_permission` and `modify_tag` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `FeedType` enum for `get_feed` method
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `FilterType` enum for `create_filter` and `modify_filter` method
  [#133](https://github.com/greenbone/python-gvm/pull/133)
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `HostsOrdering` enum for `create_task` and `modify_task` method
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `InfoType` enum for `get_info` and `get_info_list` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `PermissionSubjectType` enum for `create_permission` and
  `modify_permission` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `PortRangeType` enum for `create_port_range` method
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `ScannerType` enum for `create_scanner` and `modify_scanner` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `SnmpAuthAlgorithm` and `SnmpPrivacyAlgorithm` enums for `create_credential`
  and `modify_credential` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `SeverityLevel` enum for `create_note`, `create_override`, `modify_note`
  and `modify_override` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Use new `TimeUnit` enum for `create_schedule` and `modify_schedule` methods
  [#139](https://github.com/greenbone/python-gvm/pull/139)
* Update `create_schedule` and `modify_schedule` in `Gmpv8` to use
  [iCalendar](https://tools.ietf.org/html/rfc5545) based data for schedules
  [#140](https://github.com/greenbone/python-gvm/pull/140)

### Removed
* Removed the format parameter from `get_credentials` method [#85](https://github.com/greenbone/python-gvm/pull/85)
* Removed the task_id and nvt_oid parameters from `get_notes` and
  `get_overrides` methods [#85](https://github.com/greenbone/python-gvm/pull/85)
* Removed sources argument from `modify_user` method [#87](https://github.com/greenbone/python-gvm/pull/87)
* Removed `modify_report` method [#87](https://github.com/greenbone/python-gvm/pull/87)
* Removed unused comment argument from `create_note` and `create_override` [#87](https://github.com/greenbone/python-gvm/pull/87)
* Removed hosts_ordering argument from `modify_target` [#88](https://github.com/greenbone/python-gvm/pull/88)
* Excluded tests from installation [#119](https://github.com/greenbone/python-gvm/pull/119)
* Removed `credential_type` argument from `modify_credential` [#139](https://github.com/greenbone/python-gvm/pull/139)

### Fixed
* Fixed generating XML for `get_credentials` command [#74](https://github.com/greenbone/python-gvm/pull/74)
* Fixed generating XML for `get_settings` command [#80](https://github.com/greenbone/python-gvm/pull/80)
* Fixed generating XML for `get_nvts` command [#84](https://github.com/greenbone/python-gvm/pull/84)
* Fixed wrong order of key and value for condition_data, event_data and
  method_data dict parameters of `modify_alert` method [#85](https://github.com/greenbone/python-gvm/pull/85)
* Fixed sending resource id in `modify_tag` [#88](https://github.com/greenbone/python-gvm/pull/88)
* Ensure `modify_setting` value is send as Base64-encoded [#98](https://github.com/greenbone/python-gvm/pull/98)

### Deprecated
* `modify_config` is marked as deprecated and will be removed in future. One of
  the more specific `modify_config_set_` method should be used instead [#87](https://github.com/greenbone/python-gvm/pull/87)

[1.0.0.beta3]: https://github.com/greenbone/python-gvm/compare/v1.0.0.beta2...v1.0.0.beta3

## [1.0.0.beta2] - 2018-12-04

### Added
* Added new `trigger_alert` method for triggering an alert method on a
  specific report.
* Added `import_config` method to import a scan config from xml.
* Added helper function to validate xml input `gvm.xml.validate_xml_string`
* Add `finish_send` method to connections. The method allows to indicate to
  the server sending data is finished and no additional data has to be received.

### Changed
* `help` method `type` argument got renamed to `help_type`
* `help` method `help_type` argument will be checked for invalid values
* `create_credential` requires a credential_type argument now.
* Optional arguments are required to be passed as keyword arguments.
* `get_report` method `format_id` argument got renamed to
  `report_format_id`
* Check if scanner_type is one of '1' (OSP Scanner) or '2' (OpenVAS Scanner) in
  `create_scanner` method.
* `pretty_print` accepts a xml string as input too
* Optional arguments for connection class constructors must be passed as
  keyword arguments.
* It's possible to wait indefinitely by deactivating the timeouts via passing
  None as timeout argument to the connection class constructors now.

### Fixed
* Fix: Don't close the connection after each send/read command sequence
  automatically. This fixes sending more then one privileged gmp command after
  authentication.
* Fixed generating XML for help command
* Fixed wrong order of key and value for condition_data, event_data and
  method_data dict parameters of `create_alert` method.
* Fixed `get_reports` sending the wrong protocol command
* Fixed `create_permission` method
* Fixed `get_config` sending the correct protocol command.
* Don't crash if huge content is returned in a xml response. This fixes e.g.
  `get_reports` for bigger report data.

### Removed
* Removed `format_id` argument from get_reports
* Removed `alert_id` argument from `get_reports`
* Removed unused `read_timeout` argument from `UnixSocketConnection`

## [1.0.0.beta1] - 2018-11-13

python-gvm was a part of [gvm-tools](https://github.com/greenbone/gvm-tools)
prior gvm-tools version 2.0. It got extracted from gvm-tools and completely
overhauled.

Some notable changes are:

* The package name changed from *gmp* to *gvm*.
* The type of connection is passed to a more generic Gmp class instead of
  having to select the connection when creating the gmp object.
* Support for different protocols and versions has been added. Currently
  supported protocols are OSP v1 and GMP v7.
* Full API documentation is available at https://python-gvm.readthedocs.io/en/latest/.
* Possible arguments to protocol methods are documented.
* Arguments should be passed as keywords

### Gmp API changes

* `create_report` has been renamed to `import_report`.
* Requesting single entities has been extracted from the list commands e.g.
  `get_task(task_id)` instead of `get_tasks(task_id=task_id)`.
* `get_info` requests a single info entity.
* `get_info_list` requests a list of info entities.
* `filt_id` argument is called `filter_id` at all Gmp methods.
* `report_filter` argument for `get_reports` got renamed to `filter`.
  `report_filt_id` is `filter_id` now.
* `create_schedule` `start_time` and `end_time` arguments got split into
  several parameters.
* Plural arguments like `hosts`, `users`, ... always require a list now.
* `create_alert` `event`, `condition` and `method` arguments got
  revised and split.
* Boolean parameters expect True and False and not 1, 0, '1' or '0' now.
* `get_assets` type parameter got renamed to `asset_type`
* Copying an entity via the `copy` argument has been removed and extracted to
  own `clone` methods e.g. `clone_task`.

[1.0.0.beta2]: https://github.com/greenbone/python-gvm/compare/v1.0.0.beta1...v1.0.0.beta2
[1.0.0.beta1]: https://github.com/greenbone/python-gvm/releases/tag/v1.0.0.beta1
