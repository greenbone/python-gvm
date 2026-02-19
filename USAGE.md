# Guide complet — python-gvm

**python-gvm** est la bibliothèque Python officielle pour piloter un serveur
Greenbone Vulnerability Management (GVM) via le protocole GMP ou OSP.

---

## Table des matières

- [Installation](#installation)
- [Connexions](#connexions)
- [Transforms (format de réponse)](#transforms)
- [Gestion des erreurs](#gestion-des-erreurs)
- [GMP — Greenbone Management Protocol](#gmp--greenbone-management-protocol)
  - [Authentification](#authentification)
  - [Tâches (Tasks)](#tâches-tasks)
  - [Cibles (Targets)](#cibles-targets)
  - [Scanners](#scanners)
  - [Configurations de scan (Scan Configs)](#configurations-de-scan)
  - [Alertes (Alerts)](#alertes)
  - [Credentials](#credentials)
  - [Rapports (Reports)](#rapports-reports)
  - [Résultats (Results)](#résultats-results)
  - [Audits et politiques (Policies)](#audits-et-politiques)
  - [Planifications (Schedules)](#planifications-schedules)
  - [Filtres (Filters)](#filtres-filters)
  - [Tags](#tags)
  - [Groupes (Groups)](#groupes-groups)
  - [Rôles (Roles)](#rôles-roles)
  - [Utilisateurs (Users)](#utilisateurs-users)
  - [Permissions](#permissions)
  - [Notes](#notes)
  - [Overrides](#overrides)
  - [Tickets](#tickets)
  - [Certificats TLS](#certificats-tls)
  - [Vulnérabilités (Vulnerabilities)](#vulnérabilités)
  - [Formats de rapport (Report Formats)](#formats-de-rapport)
  - [Configurations de rapport (Report Configs) — v22.6+](#configurations-de-rapport--v226)
  - [Hôtes et systèmes d'exploitation](#hôtes-et-systèmes-dexploitation)
  - [NVTs et informations de sécurité](#nvts-et-informations-de-sécurité)
  - [CVEs, CPEs et avis CERT](#cves-cpes-et-avis-cert)
  - [Listes de ports (Port Lists)](#listes-de-ports)
  - [Feeds](#feeds)
  - [Agrégats (Aggregates)](#agrégats)
  - [Corbeille et paramètres](#corbeille-et-paramètres)
  - [Fonctionnalités GMPNext (développement)](#fonctionnalités-gmpnext)
- [OSP — Open Scanner Protocol](#osp--open-scanner-protocol)
- [HTTP / OpenVASD](#http--openvasd)
- [Utilitaires XML](#utilitaires-xml)
- [Débogage](#débogage)
- [Versions GMP supportées](#versions-gmp-supportées)

---

## Installation

```bash
python3 -m pip install python-gvm
```

Dépendances automatiquement installées : `lxml`, `paramiko`, `httpx[http2]`.

---

## Connexions

Choisissez le type de connexion adapté à votre infrastructure.

### UnixSocketConnection — socket local

```python
from gvm.connections import UnixSocketConnection

connection = UnixSocketConnection(
    path='/run/gvmd/gvmd.sock',  # par défaut : /run/gvmd/gvmd.sock
    timeout=60,                  # délai en secondes (défaut : 60)
)
```

### TLSConnection — TCP sécurisé

```python
from gvm.connections import TLSConnection

connection = TLSConnection(
    hostname='192.168.1.100',
    port=9390,                    # défaut : 9390
    certfile='/path/client.crt',  # certificat client (optionnel)
    keyfile='/path/client.key',   # clé privée client (optionnel)
    cafile='/path/ca.crt',        # CA pour vérifier le serveur (optionnel)
    password=None,                # mot de passe de la clé privée (optionnel)
    timeout=60,
)
```

### SSHConnection — tunnel SSH

```python
from gvm.connections import SSHConnection

connection = SSHConnection(
    hostname='192.168.1.100',
    port=22,                     # défaut : 22
    username='gmp',              # défaut : 'gmp'
    password='secret',           # défaut : ''
    known_hosts_file='~/.ssh/known_hosts',  # optionnel
    auto_accept_host=False,      # accepter automatiquement les hôtes inconnus
    timeout=60,
)
```

### DebugConnection — enregistrement des échanges

Enveloppe n'importe quelle connexion pour journaliser chaque commande envoyée et réponse reçue.

```python
from gvm.connections import UnixSocketConnection, DebugConnection
import logging

logging.basicConfig(filename='gvm.log', level=logging.DEBUG)
connection = DebugConnection(UnixSocketConnection())
```

---

## Transforms

Les transforms définissent le format de la valeur retournée par chaque méthode GMP/OSP.

| Classe | Retourne | Lève une erreur si status ≠ 200 |
|--------|----------|---------------------------------|
| *(aucun — défaut)* | `str` (XML brut UTF-8) | Non |
| `EtreeTransform` | `lxml.etree.Element` | Non |
| `CheckCommandTransform` | `str` | Oui |
| `EtreeCheckCommandTransform` | `lxml.etree.Element` | Oui |

```python
from gvm.transforms import EtreeCheckCommandTransform, EtreeTransform
from gvm.xml import pretty_print

# Retourne un Element ET valide le status
transform = EtreeCheckCommandTransform()

# Retourne un Element sans valider le status
transform = EtreeTransform()
```

Utilisation avec GMP :

```python
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform

with GMP(UnixSocketConnection(), transform=EtreeCheckCommandTransform()) as gmp:
    gmp.authenticate('admin', 'password')
    tasks = gmp.get_tasks()
    # tasks est un lxml.etree.Element
    for task in tasks.xpath('task'):
        print(task.find('name').text)
```

---

## Gestion des erreurs

Toutes les exceptions héritent de `GvmError`.

```
GvmError
├── GvmClientError
│   ├── GvmResponseError    # réponse avec status d'erreur
│   ├── InvalidArgument     # valeur de paramètre invalide
│   ├── InvalidArgumentType # type de paramètre incorrect
│   └── RequiredArgument    # paramètre obligatoire manquant
└── GvmServerError          # erreur retournée par le serveur
```

```python
from gvm.errors import (
    GvmError,
    GvmServerError,
    GvmResponseError,
    InvalidArgument,
    InvalidArgumentType,
    RequiredArgument,
)

try:
    with GMP(connection, transform=transform) as gmp:
        gmp.authenticate('admin', 'password')
        gmp.get_task(task_id='<uuid>')
except RequiredArgument as e:
    print(f'Paramètre manquant : {e}')
except InvalidArgument as e:
    print(f'Valeur invalide : {e}')
except GvmServerError as e:
    print(f'Erreur serveur (status={e.status}) : {e}')
except GvmError as e:
    print(f'Erreur GVM : {e}')
```

---

## GMP — Greenbone Management Protocol

Import principal :

```python
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import GMP
from gvm.transforms import EtreeCheckCommandTransform

connection = UnixSocketConnection()
transform = EtreeCheckCommandTransform()
```

Toutes les méthodes ci-dessous sont appelées à l'intérieur du bloc `with` :

```python
with GMP(connection, transform=transform) as gmp:
    gmp.authenticate('admin', 'password')
    # ... appels de méthodes
```

---

### Authentification

```python
# Se connecter au serveur GVM
gmp.authenticate(username: str, password: str)

# Obtenir la configuration des méthodes d'authentification
gmp.describe_auth()

# Modifier une méthode d'authentification (ex : LDAP, RADIUS)
gmp.modify_auth(
    group_name: str,             # nom du groupe d'authentification
    auth_conf_settings: dict,    # dict {clé: valeur} des paramètres
)

# Obtenir la version du protocole GMP supportée par le démon distant
gmp.get_version()
```

---

### Tâches (Tasks)

Les tâches définissent un scan à effectuer (cible + config + scanner).

```python
# Créer une tâche de scan
gmp.create_task(
    name: str,
    config_id: str,              # ID de la configuration de scan
    target_id: str,              # ID de la cible
    scanner_id: str,             # ID du scanner
    *,
    alterable: bool = None,
    alert_ids: list[str] = None,
    comment: str = None,
    hosts_ordering: str = None,  # 'sequential', 'random', 'reverse'
    schedule_id: str = None,
    schedule_periods: int = None,
    observers: list[str] = None,
    preferences: dict = None,
)

# Créer une tâche conteneur (sans scan, pour importer des rapports)
gmp.create_container_task(name: str, *, comment: str = None)

# Modifier une tâche existante (tous les paramètres sont optionnels)
gmp.modify_task(
    task_id: str,
    *,
    name: str = None,
    config_id: str = None,
    target_id: str = None,
    scanner_id: str = None,
    alterable: bool = None,
    alert_ids: list[str] = None,
    comment: str = None,
    hosts_ordering: str = None,
    schedule_id: str = None,
    schedule_periods: int = None,
    observers: list[str] = None,
    preferences: dict = None,
)

# Dupliquer une tâche
gmp.clone_task(task_id: str)

# Supprimer une tâche
gmp.delete_task(task_id: str, *, ultimate: bool = False)

# Récupérer toutes les tâches (avec filtres optionnels)
gmp.get_tasks(
    *,
    filter_string: str = None,   # ex: 'name~weekly rows=10'
    filter_id: str = None,       # ID d'un filtre sauvegardé
    trash: bool = None,          # tâches dans la corbeille
    details: bool = None,
    schedules_only: bool = None,
)

# Récupérer une tâche par son ID
gmp.get_task(task_id: str)

# Déplacer une tâche vers un esclave (sensor)
gmp.move_task(task_id: str, *, slave_id: str = None)

# Démarrer, arrêter, reprendre un scan
gmp.start_task(task_id: str)
gmp.stop_task(task_id: str)
gmp.resume_task(task_id: str)
```

---

### Cibles (Targets)

Les cibles définissent quels hôtes/ports scanner.

```python
# Créer une cible
gmp.create_target(
    name: str,
    *,
    hosts: list[str] = None,           # liste d'IPs ou noms de domaine
    exclude_hosts: list[str] = None,
    comment: str = None,
    alive_test: str = None,            # 'ICMP Ping', 'TCP-ACK Service Ping', etc.
    allow_simultaneous_ips: bool = None,
    asset_hosts_filter: str = None,
    esxi_credential_id: str = None,
    krb5_credential_id: str = None,
    port_list_id: str = None,
    port_range: str = None,
    smb_credential_id: str = None,
    snmp_credential_id: str = None,
    ssh_credential_id: str = None,
    ssh_credential_port: int = None,
    reverse_lookup_only: bool = None,
    reverse_lookup_unify: bool = None,
)

# Modifier une cible (tous les paramètres sont optionnels)
gmp.modify_target(target_id: str, *, name=None, hosts=None, ...)

# Dupliquer, supprimer, récupérer
gmp.clone_target(target_id: str)
gmp.delete_target(target_id: str, *, ultimate: bool = False)
gmp.get_target(target_id: str, *, tasks: bool = None)
gmp.get_targets(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
    tasks: bool = None,
)
```

---

### Scanners

```python
# Créer un scanner
gmp.create_scanner(
    name: str,
    host: str,
    port: int,
    scanner_type: ScannerType,   # ScannerType.OPENVAS, ScannerType.GMP, etc.
    credential_id: str,
    *,
    ca_pub: str = None,
    comment: str = None,
    relay_host: str = None,      # v22.7+ : hôte relais
    relay_port: int = None,      # v22.7+ : port relais
)

# Modifier un scanner
gmp.modify_scanner(
    scanner_id: str,
    *,
    name: str = None,
    host: str = None,
    port: int = None,
    scanner_type: ScannerType = None,
    credential_id: str = None,
    ca_pub: str = None,
    comment: str = None,
    relay_host: str = None,
    relay_port: int = None,
)

gmp.clone_scanner(scanner_id: str)
gmp.delete_scanner(scanner_id: str, ultimate: bool = False)
gmp.get_scanner(scanner_id: str)
gmp.get_scanners(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
    details: bool = None,
)
gmp.verify_scanner(scanner_id: str)
```

Types disponibles via `from gvm.protocols.gmp.requests import ScannerType` :
`OPENVAS`, `CVE`, `GMP`, `GREENBONE_SENSOR`.

---

### Configurations de scan

```python
# Créer une config de scan à partir d'une config existante (base)
gmp.create_scan_config(
    config_id: str,   # ID de la config à utiliser comme base
    name: str,
    *,
    comment: str = None,
)

# Importer une config au format XML
gmp.import_scan_config(config: str)   # chaîne XML complète

gmp.clone_scan_config(config_id: str)
gmp.delete_scan_config(config_id: str, *, ultimate: bool = False)
gmp.get_scan_config(config_id: str, *, tasks: bool = None)
gmp.get_scan_configs(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
    details: bool = None,
    families: bool = None,
    preferences: bool = None,
    tasks: bool = None,
)

# Récupérer les préférences d'une config
gmp.get_scan_config_preferences(
    *,
    nvt_oid: str = None,
    config_id: str = None,
)
gmp.get_scan_config_preference(
    name: str,
    *,
    nvt_oid: str = None,
    config_id: str = None,
)

# Récupérer les NVTs d'une config
gmp.get_scan_config_nvts(
    *,
    details: bool = None,
    preferences: bool = None,
    preference_count: bool = None,
    timeout: bool = None,
    config_id: str = None,
    preferences_config_id: str = None,
    family: str = None,
    sort_order: str = None,
    sort_field: str = None,
)
gmp.get_scan_config_nvt(nvt_oid: str)

# Modifier une config de scan
gmp.modify_scan_config_set_name(config_id: str, name: str)
gmp.modify_scan_config_set_comment(config_id: str, *, comment: str = None)
gmp.modify_scan_config_set_nvt_preference(
    config_id: str,
    name: str,
    nvt_oid: str,
    *,
    value: str = None,
)
gmp.modify_scan_config_set_scanner_preference(
    config_id: str,
    name: str,
    *,
    value: str = None,
)
gmp.modify_scan_config_set_nvt_selection(
    config_id: str,
    family: str,
    nvt_oids: list[str],
)
gmp.modify_scan_config_set_family_selection(
    config_id: str,
    families: list[tuple],   # liste de (nom, growing, include_all)
    *,
    auto_add_new_families: bool = True,
)
```

---

### Alertes

Les alertes déclenchent des actions automatiques (email, syslog, etc.) en réponse à des événements.

```python
# Créer une alerte
gmp.create_alert(
    name: str,
    condition: AlertCondition,   # ex: AlertCondition.ALWAYS
    event: AlertEvent,           # ex: AlertEvent.TASK_RUN_STATUS_CHANGED
    method: AlertMethod,         # ex: AlertMethod.EMAIL
    *,
    method_data: dict = None,    # paramètres de la méthode
    event_data: dict = None,     # paramètres de l'événement
    condition_data: dict = None, # paramètres de la condition
    filter_id: str = None,
    comment: str = None,
)

gmp.modify_alert(alert_id: str, *, name=None, condition=None, ...)
gmp.clone_alert(alert_id: str)
gmp.delete_alert(alert_id: str, *, ultimate: bool = False)
gmp.get_alert(alert_id: str, *, tasks: bool = None)
gmp.get_alerts(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
    tasks: bool = None,
)

# Tester une alerte (envoi de test)
gmp.test_alert(alert_id: str)

# Déclencher une alerte sur un rapport existant
gmp.trigger_alert(
    alert_id: str,
    report_id: str,
    *,
    filter_string: str = None,
    filter_id: str = None,
    report_format_id: str = None,
    ignore_pagination: bool = None,
    details: bool = None,
)
```

---

### Credentials

```python
# Créer un credential (identifiants pour les scans authentifiés)
gmp.create_credential(
    name: str,
    credential_type: CredentialType,  # CredentialType.USERNAME_PASSWORD, etc.
    *,
    comment: str = None,
    allow_insecure: bool = None,
    certificate: str = None,
    key_phrase: str = None,
    private_key: str = None,
    login: str = None,
    password: str = None,
    auth_algorithm: SnmpAuthAlgorithm = None,   # pour SNMP
    community: str = None,                       # pour SNMP
    privacy_algorithm: SnmpPrivacyAlgorithm = None,
    privacy_password: str = None,
    public_key: str = None,
)

gmp.modify_credential(credential_id: str, *, name=None, ...)
gmp.clone_credential(credential_id: str)
gmp.delete_credential(credential_id: str, *, ultimate: bool = False)
gmp.get_credential(
    credential_id: str,
    *,
    scanners: bool = None,
    targets: bool = None,
    credential_format: CredentialFormat = None,
)
gmp.get_credentials(
    *,
    filter_string: str = None,
    filter_id: str = None,
    scanners: bool = None,
    trash: bool = None,
    targets: bool = None,
)
```

Types de credentials (`CredentialType`) : `USERNAME_PASSWORD`, `USERNAME_SSH_KEY`,
`CLIENT_CERTIFICATE`, `KRB5`, `SMIME`, `PGP`, `PASSWORD_ONLY`, `SNMP`.

---

### Rapports (Reports)

```python
# Récupérer un rapport
gmp.get_report(
    report_id: str,
    *,
    filter_string: str = None,
    filter_id: str = None,
    report_format_id: str = None,    # format de sortie (PDF, XML, CSV...)
    ignore_pagination: bool = None,
    details: bool = None,
)

# Récupérer tous les rapports
gmp.get_reports(
    *,
    filter_string: str = None,
    filter_id: str = None,
    note_details: bool = None,
    override_details: bool = None,
    details: bool = None,
    ignore_pagination: bool = None,
    report_format_id: str = None,
)

# Supprimer un rapport
gmp.delete_report(report_id: str)

# Importer un rapport dans une tâche conteneur
gmp.import_report(
    report: str,         # XML du rapport
    task_id: str,
    *,
    in_assets: bool = None,
)

# v22.6+ : rapports d'audit séparés
gmp.get_audit_report(report_id: str, *, ...)
gmp.get_audit_reports(*, ...)
gmp.delete_audit_report(report_id: str)
```

---

### Résultats (Results)

```python
gmp.get_result(result_id: str)
gmp.get_results(
    *,
    filter_string: str = None,
    filter_id: str = None,
    task_id: str = None,
    note_details: bool = None,
    override_details: bool = None,
    ignore_pagination: bool = None,
    details: bool = None,
)
```

---

### Audits et politiques

Les **politiques** (policies) sont l'équivalent des configurations de scan pour les audits de conformité.

```python
# Politiques
gmp.create_policy(name: str, *, policy_id: str = None, comment: str = None)
gmp.import_policy(policy: str)                   # XML
gmp.clone_policy(policy_id: str)
gmp.delete_policy(policy_id: str, *, ultimate: bool = False)
gmp.get_policy(policy_id: str, *, audits: bool = None)
gmp.get_policies(
    *,
    audits: bool = None,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
)
gmp.modify_policy_set_name(policy_id: str, name: str)
gmp.modify_policy_set_comment(policy_id: str, comment: str = None)
gmp.modify_policy_set_nvt_preference(policy_id, name, nvt_oid, *, value=None)
gmp.modify_policy_set_scanner_preference(policy_id, name, *, value=None)
gmp.modify_policy_set_nvt_selection(policy_id, family, nvt_oids)
gmp.modify_policy_set_family_selection(policy_id, families, *, auto_add_new_families=True)

# Audits (identique aux tâches mais pour les politiques de conformité)
gmp.create_audit(
    name: str,
    policy_id: str,
    target_id: str,
    scanner_id: str,
    *, ...            # mêmes options que create_task
)
gmp.modify_audit(audit_id: str, *, ...)
gmp.clone_audit(audit_id: str)
gmp.delete_audit(audit_id: str, *, ultimate: bool = False)
gmp.get_audit(audit_id: str)
gmp.get_audits(*, filter_string=None, filter_id=None, trash=None, details=None, ...)
gmp.start_audit(audit_id: str)
gmp.stop_audit(audit_id: str)
gmp.resume_audit(audit_id: str)
```

---

### Planifications (Schedules)

Les planifications utilisent le format **iCalendar (RFC 5545)**.

```python
# Créer une planification
gmp.create_schedule(
    name: str,
    icalendar: str,     # données iCal (VCALENDAR/VEVENT)
    timezone: str,      # ex: 'Europe/Paris'
    *,
    comment: str = None,
)

gmp.modify_schedule(
    schedule_id: str,
    *,
    name: str = None,
    icalendar: str = None,
    timezone: str = None,
    comment: str = None,
)
gmp.clone_schedule(schedule_id: str)
gmp.delete_schedule(schedule_id: str, *, ultimate: bool = False)
gmp.get_schedule(schedule_id: str, *, tasks: bool = None)
gmp.get_schedules(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
    tasks: bool = None,
)
```

Exemple de chaîne iCal pour une planification hebdomadaire le lundi à 3h :

```python
ical = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART:20240101T030000Z
RRULE:FREQ=WEEKLY;BYDAY=MO
END:VEVENT
END:VCALENDAR"""
gmp.create_schedule(name='Hebdo lundi', icalendar=ical, timezone='UTC')
```

---

### Filtres (Filters)

Les filtres sauvegardés peuvent être réutilisés dans les requêtes `get_*`.

```python
# Créer un filtre
gmp.create_filter(
    name: str,
    *,
    filter_type: FilterType = None,  # FilterType.TASK, FilterType.REPORT, etc.
    comment: str = None,
    term: str = None,                # expression du filtre, ex: 'name~weekly rows=10'
)

gmp.modify_filter(
    filter_id: str,
    *,
    name: str = None,
    filter_type: FilterType = None,
    comment: str = None,
    term: str = None,
)
gmp.clone_filter(filter_id: str)
gmp.delete_filter(filter_id: str, *, ultimate: bool = False)
gmp.get_filter(filter_id: str, *, alerts: bool = None)
gmp.get_filters(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
)
```

---

### Tags

```python
gmp.create_tag(
    name: str,
    resource_type: EntityType,
    *,
    active: bool = None,
    comment: str = None,
    resource_filter: str = None,
    resource_ids: list[str] = None,
    value: str = None,
)
gmp.modify_tag(
    tag_id: str,
    *,
    name: str = None,
    resource_type: EntityType = None,
    active: bool = None,
    comment: str = None,
    resource_filter: str = None,
    resource_ids: list[str] = None,
    value: str = None,
)
gmp.clone_tag(tag_id: str)
gmp.delete_tag(tag_id: str, *, ultimate: bool = False)
gmp.get_tag(tag_id: str)
gmp.get_tags(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
    names_only: bool = None,
)
```

---

### Groupes (Groups)

```python
gmp.create_group(
    name: str,
    *,
    comment: str = None,
    special: bool = False,    # accès "super" à toutes les ressources
    users: list[str] = None,
)
gmp.modify_group(
    group_id: str,
    *,
    name: str = None,
    comment: str = None,
    special: bool = None,
    users: list[str] = None,
)
gmp.clone_group(group_id: str)
gmp.delete_group(group_id: str, *, ultimate: bool = False)
gmp.get_group(group_id: str)
gmp.get_groups(*, filter_string=None, filter_id=None, trash=None)
```

---

### Rôles (Roles)

```python
gmp.create_role(name: str, *, comment: str = None, users: list[str] = None)
gmp.modify_role(
    role_id: str,
    *,
    name: str = None,
    comment: str = None,
    users: list[str] = None,
)
gmp.clone_role(role_id: str)
gmp.delete_role(role_id: str, *, ultimate: bool = False)
gmp.get_role(role_id: str)
gmp.get_roles(*, filter_string=None, filter_id=None, trash=None)
```

---

### Utilisateurs (Users)

```python
gmp.create_user(
    name: str,
    *,
    password: str = None,
    hosts: list[str] = None,        # hôtes autorisés (None = tous)
    hosts_allow: bool = False,       # True = liste blanche, False = liste noire
    role_ids: list[str] = None,
)
gmp.modify_user(
    user_id: str,
    *,
    name: str = None,
    password: str = None,
    hosts: list[str] = None,
    hosts_allow: bool = None,
    role_ids: list[str] = None,
    sources: list[str] = None,       # sources d'authentification
)
gmp.clone_user(user_id: str)
gmp.delete_user(
    *,
    user_id: str = None,
    name: str = None,
    inheritor_id: str = None,     # utilisateur qui hérite des ressources
    inheritor_name: str = None,
)
gmp.get_user(user_id: str)
gmp.get_users(*, filter_string=None, filter_id=None)
```

---

### Permissions

```python
gmp.create_permission(
    name: str,              # nom de la commande GMP autorisée
    subject_id: str,        # ID de l'utilisateur/groupe/rôle
    subject_type: str,      # 'user', 'group', 'role'
    *,
    object_id: str = None,
    object_type: str = None,
    comment: str = None,
)
gmp.modify_permission(
    permission_id: str,
    *,
    name: str = None,
    comment: str = None,
    subject_id: str = None,
    subject_type: str = None,
    resource_id: str = None,
    resource_type: str = None,
)
gmp.clone_permission(permission_id: str)
gmp.delete_permission(permission_id: str, *, ultimate: bool = False)
gmp.get_permission(permission_id: str)
gmp.get_permissions(*, filter_string=None, filter_id=None, trash=None)
```

---

### Notes

Les notes sont des annotations textuelles attachées à des NVTs ou résultats.

```python
gmp.create_note(
    text: str,
    nvt_oid: str,
    *,
    days_active: int = None,    # -1 = illimité, 0 = inactif, N = N jours
    hosts: list[str] = None,
    port: str = None,
    result_id: str = None,
    severity: float = None,
    task_id: str = None,
)
gmp.modify_note(
    note_id: str,
    text: str,
    *,
    days_active: int = None,
    hosts: list[str] = None,
    port: str = None,
    result_id: str = None,
    severity: float = None,
    task_id: str = None,
)
gmp.clone_note(note_id: str)
gmp.delete_note(note_id: str, *, ultimate: bool = False)
gmp.get_note(note_id: str)
gmp.get_notes(
    *,
    filter_string: str = None,
    filter_id: str = None,
    details: bool = None,
    result: bool = None,
    task: bool = None,
    trash: bool = None,
)
```

---

### Overrides

Les overrides modifient la sévérité affichée d'un résultat spécifique.

```python
gmp.create_override(
    text: str,
    nvt_oid: str,
    *,
    days_active: int = None,
    hosts: list[str] = None,
    port: str = None,
    result_id: str = None,
    severity: float = None,     # sévérité originale (condition)
    new_severity: float = None, # sévérité affichée à la place
    task_id: str = None,
)
gmp.modify_override(override_id: str, text: str, *, ...)
gmp.clone_override(override_id: str)
gmp.delete_override(override_id: str, *, ultimate: bool = False)
gmp.get_override(override_id: str)
gmp.get_overrides(*, filter_string=None, filter_id=None, details=None, ...)
```

---

### Tickets

Les tickets permettent de suivre la remédiation des vulnérabilités.

```python
gmp.create_ticket(
    *,
    result_id: str,
    assigned_to_user_id: str,
    note: str,
    comment: str = None,
)
gmp.modify_ticket(
    ticket_id: str,
    *,
    status: TicketStatus = None,    # TicketStatus.OPEN, FIXED, CLOSED
    assigned_to_user_id: str = None,
    note: str = None,
    open_note: str = None,
    fixed_note: str = None,
    closed_note: str = None,
    comment: str = None,
)
gmp.clone_ticket(ticket_id: str)
gmp.delete_ticket(ticket_id: str, *, ultimate: bool = False)
gmp.get_ticket(ticket_id: str)
gmp.get_tickets(*, filter_string=None, filter_id=None, trash=None)
```

---

### Certificats TLS

```python
gmp.create_tls_certificate(
    name: str,
    certificate: str,     # PEM
    *,
    comment: str = None,
    trust: bool = None,
)
gmp.modify_tls_certificate(
    tls_certificate_id: str,
    *,
    name: str = None,
    comment: str = None,
    trust: bool = None,
)
gmp.clone_tls_certificate(tls_certificate_id: str)
gmp.delete_tls_certificate(tls_certificate_id: str)
gmp.get_tls_certificate(tls_certificate_id: str)
gmp.get_tls_certificates(
    *,
    filter_string: str = None,
    filter_id: str = None,
    include_certificate_data: bool = None,
)
```

---

### Vulnérabilités

```python
gmp.get_vulnerability(vulnerability_id: str)
gmp.get_vulnerabilities(
    *,
    filter_string: str = None,
    filter_id: str = None,
)
```

---

### Formats de rapport

```python
gmp.clone_report_format(report_format_id: str)
gmp.delete_report_format(report_format_id: str, *, ultimate: bool = False)
gmp.get_report_format(report_format_id: str)
gmp.get_report_formats(
    *,
    filter_string: str = None,
    filter_id: str = None,
    trash: bool = None,
    alerts: bool = None,
    params: bool = None,
    details: bool = None,
)
gmp.import_report_format(report_format: str)    # XML
gmp.modify_report_format(
    report_format_id: str,
    *,
    active: bool = None,
    name: str = None,
    summary: str = None,
    param_name: str = None,
    param_value: str = None,
)
gmp.verify_report_format(report_format_id: str)
```

---

### Configurations de rapport — v22.6+

```python
gmp.create_report_config(
    name: str,
    report_format_id: str,
    *,
    comment: str = None,
    params: list = None,    # liste de ReportConfigParameter
)
gmp.modify_report_config(
    report_config_id: str,
    *,
    name: str = None,
    comment: str = None,
    params: list = None,
)
gmp.clone_report_config(report_config_id: str)
gmp.delete_report_config(report_config_id: str, *, ultimate: bool = False)
gmp.get_report_config(report_config_id: str)
gmp.get_report_configs(*, filter_string=None, filter_id=None, trash=None)
```

---

### Hôtes et systèmes d'exploitation

```python
# Hôtes (assets)
gmp.create_host(name: str, *, comment: str = None)
gmp.modify_host(host_id: str, *, comment: str = None)
gmp.delete_host(host_id: str)
gmp.get_host(host_id: str, *, details: bool = None)
gmp.get_hosts(*, filter_string=None, filter_id=None, details=None)

# Systèmes d'exploitation (assets)
gmp.modify_operating_system(operating_system_id: str, *, comment: str = None)
gmp.delete_operating_system(operating_system_id: str)
gmp.get_operating_system(operating_system_id: str, *, details: bool = None)
gmp.get_operating_systems(*, filter_string=None, filter_id=None, details=None)
```

---

### NVTs et informations de sécurité

```python
# NVTs (Network Vulnerability Tests)
gmp.get_nvt(nvt_id: str, *, extended: bool = None)
gmp.get_nvts(
    *,
    filter_string: str = None,
    filter_id: str = None,
    details: bool = None,
    preferences: bool = None,
    preference_count: bool = None,
    timeout: bool = None,
    config_id: str = None,
    preferences_config_id: str = None,
    family: str = None,
    sort_order: str = None,
    sort_field: str = None,
)
gmp.get_nvt_families(*, sort_order: str = None)
gmp.get_nvt_preferences(*, nvt_oid: str = None)
gmp.get_nvt_preference(name: str, *, nvt_oid: str = None)

# Informations de sécurité génériques
gmp.get_info(info_id: str, info_type: InfoType)
gmp.get_info_list(
    info_type: InfoType,   # InfoType.CVE, CPE, NVT, OVALDEF, etc.
    *,
    filter_string: str = None,
    filter_id: str = None,
    name: str = None,
    details: bool = None,
)
```

---

### CVEs, CPEs et avis CERT

```python
# CVEs
gmp.get_cve(cve_id: str)
gmp.get_cves(*, filter_string=None, filter_id=None, details=None, ...)

# CPEs
gmp.get_cpe(cpe_id: str)
gmp.get_cpes(*, filter_string=None, filter_id=None, details=None, ...)

# Avis DFN-CERT
gmp.get_dfn_cert_advisory(cert_id: str)
gmp.get_dfn_cert_advisories(*, filter_string=None, filter_id=None, ...)

# Avis CERT-Bund
gmp.get_cert_bund_advisory(cert_id: str)
gmp.get_cert_bund_advisories(*, filter_string=None, filter_id=None, ...)
```

---

### Listes de ports

```python
gmp.create_port_list(
    name: str,
    port_range: str,       # ex: 'T:1-1024,U:53'
    *,
    comment: str = None,
)
gmp.create_port_range(
    port_list_id: str,
    start: int,
    end: int,
    port_range_type: PortRangeType,   # PortRangeType.TCP ou UDP
    *,
    comment: str = None,
)
gmp.modify_port_list(port_list_id: str, *, name: str = None, comment: str = None)
gmp.clone_port_list(port_list_id: str)
gmp.delete_port_list(port_list_id: str, *, ultimate: bool = False)
gmp.delete_port_range(port_range_id: str)
gmp.get_port_list(port_list_id: str)
gmp.get_port_lists(
    *,
    filter_string: str = None,
    filter_id: str = None,
    details: bool = None,
    targets: bool = None,
    trash: bool = None,
)
```

---

### Feeds

```python
gmp.get_feeds()                             # tous les feeds
gmp.get_feed(feed_type: FeedType)           # FeedType.NVT, CERT, SCAP, GVMD_DATA
```

---

### Agrégats

Les agrégats permettent d'obtenir des statistiques sur les ressources.

```python
gmp.get_aggregates(
    resource_type: EntityType,    # EntityType.TASK, REPORT, RESULT, etc.
    *,
    filter_string: str = None,
    filter_id: str = None,
    sort_criteria: list = None,
    data_columns: list = None,
    group_column: str = None,
    subgroup_column: str = None,
    text_columns: list = None,
    first_group: int = None,
    max_groups: int = None,
    mode: str = None,
)
```

---

### Corbeille et paramètres

```python
# Vider définitivement la corbeille
gmp.empty_trashcan()

# Restaurer un élément depuis la corbeille
gmp.restore_from_trashcan(entity_id: str)

# Paramètres de l'utilisateur courant
gmp.get_user_settings(*, filter_string: str = None)
gmp.get_user_setting(setting_id: str)
gmp.modify_user_setting(
    *,
    setting_id: str = None,
    name: str = None,
    value: str = None,
)

# Rapports système (performances)
gmp.get_system_reports(
    *,
    name: str = None,
    duration: int = None,
    start_time: str = None,
    end_time: str = None,
    brief: bool = None,
    slave_id: str = None,
)

# Aide en ligne du protocole GMP
gmp.help(*, help_format: HelpFormat = None, brief: bool = None)

# Noms de ressources — v22.6+
gmp.get_resource_names(resource_type: ResourceType, *, filter_string: str = None)
gmp.get_resource_name(resource_id: str, resource_type: ResourceType)
```

---

### Fonctionnalités GMPNext

> Ces fonctionnalités font partie de la version de développement (`GMPNext`) et peuvent changer.

```python
from gvm.protocols.gmp import GMPNext

with GMPNext(connection, transform=transform) as gmp:
    gmp.authenticate('admin', 'password')
    # ...
```

**Agents :**

```python
gmp.get_agent_installers(*, filter_string=None, filter_id=None, details=None)
gmp.get_agent_installer(agent_installer_id: str)
gmp.get_agent_installer_file(agent_installer_id: str)
gmp.get_agents(*, filter_string=None, filter_id=None, details=None)
gmp.modify_agents(
    agent_ids: list[str],
    *,
    authorized: bool = None,
    update_to_latest: bool = None,
    config: dict = None,
    comment: str = None,
)
gmp.delete_agents(agent_ids: list[str])
gmp.modify_agent_control_scan_config(agent_control_id: str, config: dict)
```

**Groupes d'agents :**

```python
gmp.create_agent_group(name: str, agent_ids: list[str], *, comment: str = None)
gmp.modify_agent_group(agent_group_id: str, *, name=None, agent_ids=None, comment=None)
gmp.clone_agent_group(agent_group_id: str)
gmp.delete_agent_group(agent_group_id: str, ultimate: bool = False)
gmp.get_agent_group(agent_group_id: str)
gmp.get_agent_groups(*, filter_string=None, filter_id=None, details=None)
```

**Tâches avec groupes d'agents :**

```python
gmp.create_agent_group_task(
    name: str,
    config_id: str,
    target_id: str,
    scanner_id: str,
    agent_group_id: str,
    *, ...
)
gmp.create_container_image_task(name: str, *, comment: str = None)
gmp.create_import_task(name: str, *, comment: str = None)
```

**Cibles OCI (conteneurs) :**

```python
gmp.create_oci_image_target(
    name: str,
    image_references: list[str],
    *,
    comment: str = None,
    credential_id: str = None,
)
gmp.modify_oci_image_target(oci_image_target_id: str, *, ...)
gmp.clone_oci_image_target(oci_image_target_id: str)
gmp.delete_oci_image_target(oci_image_target_id: str, *, ultimate: bool = False)
gmp.get_oci_image_target(oci_image_target_id: str, *, tasks: bool = None)
gmp.get_oci_image_targets(*, filter_string=None, filter_id=None, ...)
```

**Dépôts de credentials :**

```python
gmp.create_credential_store_credential(
    name: str,
    credential_type: CredentialStoreCredentialType,
    *,
    comment: str = None,
    credential_store_id: str = None,
    vault_id: str = None,
    host_identifier: str = None,
)
gmp.modify_credential_store_credential(credential_id: str, *, ...)
gmp.get_credential_store(credential_store_id: str, *, details: bool = None)
gmp.get_credential_stores(*, filter_string=None, filter_id=None, ...)
gmp.modify_credential_store(credential_store_id: str, *, ...)
gmp.verify_credential_store(credential_store_id: str)
```

---

## OSP — Open Scanner Protocol

```python
from gvm.connections import UnixSocketConnection
from gvm.protocols.latest import Osp

osp = Osp(connection=UnixSocketConnection(path='/var/run/ospd.sock'))

with osp:
    # Version du protocole (statique : 1.2)
    print(Osp.get_protocol_version())   # (1, 2)

    # Version du démon OSPD et du scanner sous-jacent
    osp.get_version()

    # Aide du protocole
    osp.help()

    # Détails du scanner (description, paramètres)
    osp.get_scanner_details()

    # Informations sur les VTs disponibles
    osp.get_vts(vt_id=None)            # tous les VTs
    osp.get_vts(vt_id='1.3.6.1...')   # un VT spécifique

    # Lancer un scan
    osp.start_scan(
        scan_id=None,          # UUID optionnel (généré si absent)
        parallel=1,
        targets=[{
            'hosts': '192.168.1.0/24',
            'ports': '80,443,8080',
        }],
        scanner_params={'key': 'value'},
        vt_selection={
            '1.3.6.1.4.1.25623.1.0.90022': {},  # OID: {paramètres}
        },
    )

    # État et résultats d'un scan
    osp.get_scans(
        scan_id=None,           # None = tous les scans
        details=True,
        pop_results=False,      # True = consomme et vide les résultats
    )

    # Arrêter un scan
    osp.stop_scan(scan_id='<uuid>')

    # Supprimer les données d'un scan terminé
    osp.delete_scan(scan_id='<uuid>')
```

---

## HTTP / OpenVASD

Interface HTTP vers le démon OpenVAS (`openvasd`).

```python
from gvm.protocols.http.openvasd import create_openvasd_http_client

client = create_openvasd_http_client(
    host_name='127.0.0.1',
    port=3000,
    api_key='mon-api-key',
    server_ca_path='/path/ca.pem',       # optionnel
    client_cert_paths=('/path/cert.pem', '/path/key.pem'),  # optionnel
)
```

### Health

```python
client.health.get_alive()    # 200 si le service répond
client.health.get_ready()    # 200 si le service est prêt
client.health.get_started()  # 200 si le service a démarré
```

### Metadata

```python
client.metadata.get()           # informations générales
client.metadata.get_scans()     # capacités de scan
```

### Scans

```python
from gvm.protocols.http.openvasd.scans import Target, Port, PortRange, Credential

# Créer un scan
scan_id = client.scans.create(
    target=Target(
        hosts=['192.168.1.1', '192.168.1.2'],
        ports=[Port(protocol='tcp', range=[PortRange(start=1, end=1024)])],
        credentials=[Credential(service='ssh', ...)],
    ),
    scanner_preferences=[],
    vt_selection=[],
)

# Démarrer / arrêter
client.scans.start(scan_id)
client.scans.stop(scan_id)

# Résultats
client.scans.get_status(scan_id)
client.scans.get_results(scan_id)
client.scans.get_result(scan_id, result_id)

# Liste / détail / suppression
client.scans.get_all()
client.scans.get(scan_id)
client.scans.delete(scan_id)

# Préférences du scanner
client.scans.get_preferences()
```

### VTs et Notus

```python
client.vts.get_all()              # tous les VTs disponibles
client.vts.get(oid='1.3.6.1...') # un VT spécifique

client.notus.get_os_list()            # systèmes supportés par Notus
client.notus.run_scan(os='debian:11', package_list=['libc6=2.31'])
```

---

## Utilitaires XML

```python
from gvm.xml import XmlCommand, pretty_print, parse_xml

# Construire une commande XML à la main
cmd = XmlCommand('get_tasks')
cmd.set_attribute('filter', 'name~weekly')
cmd.add_element('details', '1')
print(cmd.to_string())
# <get_tasks filter="name~weekly"><details>1</details></get_tasks>

# Parser une réponse XML brute
element = parse_xml('<get_version_response status="200"><version>22.4</version></get_version_response>')

# Afficher du XML de façon lisible
pretty_print(element)
```

---

## Débogage

```python
import logging
from gvm.connections import UnixSocketConnection, DebugConnection
from gvm.protocols.gmp import GMP

logging.basicConfig(filename='gvm.log', level=logging.DEBUG)

connection = DebugConnection(UnixSocketConnection())

with GMP(connection=connection) as gmp:
    gmp.get_version()
```

Contenu du fichier `gvm.log` :

```
DEBUG:gvm.connections:Sending 14 characters. Data <get_version/>
DEBUG:gvm.connections:Read 97 characters. Data <get_version_response status="200" status_text="OK"><version>22.4</version></get_version_response>
```

---

## Versions GMP supportées

| Classe | Version GMP | Nouveautés principales |
|--------|-------------|------------------------|
| `GMPv224` | 22.4 | Base complète (203+ méthodes) |
| `GMPv225` | 22.5 | Mises à jour mineures |
| `GMPv226` | 22.6 | Report Configs, Audit Reports séparés, Resource Names |
| `GMPv227` | 22.7 | Scanner avec relais (`relay_host`, `relay_port`) |
| `GMPNext` | dev | Agents, groupes d'agents, cibles OCI, credential stores |
| `GMP` | auto | Sélectionne automatiquement la version supportée par le serveur |

```python
# Sélection automatique (recommandé)
from gvm.protocols.gmp import GMP

# Version fixe explicite
from gvm.protocols.gmp import GMPv227, GMPv226

# Version de développement
from gvm.protocols.gmp import GMPNext
```

---

## Liens utiles

- Documentation complète : <https://greenbone.github.io/python-gvm/>
- Forum communautaire : <https://forum.greenbone.net/>
- Issues GitHub : <https://github.com/greenbone/python-gvm/issues>
