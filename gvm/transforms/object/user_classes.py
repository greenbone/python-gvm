import datetime
from dataclasses import dataclass
from lxml import etree

# from gvm.protocols.gmp import Gmp

from .utils import (
    get_bool_from_element,
    get_int_from_element,
    get_text_from_element,
    get_datetime_from_element,
)


@dataclass
class Owner:
    name: str

    @staticmethod
    def resolve_owner(root: etree.Element) -> "Owner":
        if root is None:
            return None
        name = root.find('name').text
        if name is None:
            return None
        else:
            return Owner(name)


@dataclass
class Tag:
    uuid: str
    name: str
    value: str
    comment: str

    @staticmethod
    def resolve_tags(root: etree.Element) -> list:
        if root is None:
            return None

        tags = []
        for child in root:
            if child.tag == "tag":
                tags.append(Tag.resolve_tag(child))

        return tags

    @staticmethod
    def resolve_tag(root: etree.Element) -> "Tag":
        if root is None:
            return None

        uuid = root.get("id")
        name = get_text_from_element(root, "name")
        value = get_text_from_element(root, "value")
        comment = get_text_from_element(root, "comment")

        return Tag(uuid, name, value, comment)


@dataclass
class UserTags:
    count: int
    tags: list

    @staticmethod
    def resolve_user_tags(root: etree.Element) -> "UserTags":
        count = get_int_from_element(root, "count")
        tags = Tag.resolve_tags(root)

        return UserTags(count, tags)


@dataclass
class Permission:
    name: str

    @staticmethod
    def resolve_permissions(root: etree.Element) -> list:
        if root is None:
            return None
        permissions = []
        for permission in root:
            permissions.append(Permission(permission.find("name").text))

        if len(permissions) == 1:
            return permissions[0]
        else:
            return permissions


@dataclass
class Group:
    gmp: "Gmp"
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    permissions: list
    user_tags: UserTags
    users: list

    @staticmethod
    def resolve_groups(root: etree.Element, gmp):
        if root is None:
            return None

        groups = []
        for child in root:
            if child.tag == "group":
                groups.append(Group.resolve_group(child, gmp))

        if len(groups) == 1:
            return groups[0]
        return groups

    @staticmethod
    def resolve_group(root: etree.Element, gmp):
        if root is None:
            return None

        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = get_text_from_element(root, "name")
        comment = get_text_from_element(root, "comment")
        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")
        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")
        permissions = Permission.resolve_permissions(root.find("permissions"))
        user_tags = UserTags.resolve_user_tags(root.find("user_tags"))

        users = get_text_from_element(root, "users")
        if users is not None:
            users = users.replace(" ", "")
            users = users.split(",")

        return Group(
            gmp,
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            permissions,
            user_tags,
            users,
        )


@dataclass
class User:
    uuid: str
    owner: Owner
    name: str
    comment: str
    creation_time: datetime.datetime
    modification_time: datetime.datetime
    writable: bool
    in_use: bool
    # role
    groups: Group
    # hosts
    # ifaces
    permissions: list
    user_tags: UserTags
    # sources

    @staticmethod
    def resolve_users(root: etree.Element, gmp) -> list:
        if root is None:
            return None

        users = []

        for child in root:
            if child.tag == "user":
                users.append(User.resolve_user(child, gmp))

        return users

    @staticmethod
    def resolve_user(root: etree.Element, gmp) -> "User":
        uuid = root.get("id")
        owner = Owner.resolve_owner(root.find("owner"))
        name = get_text_from_element(root, "name")
        comment = get_text_from_element(root, "comment")
        creation_time = get_datetime_from_element(root, "creation_time")
        modification_time = get_datetime_from_element(root, "modification_time")
        writable = get_bool_from_element(root, "writable")
        in_use = get_bool_from_element(root, "in_use")
        # role
        groups = Group.resolve_groups(root.find("groups"), gmp)
        # hosts
        # ifaces
        permissions = Permission.resolve_permissions(root.find("permissions"))
        user_tags = UserTags.resolve_user_tags(root.find("user_tags"))
        # sources

        user = User(
            uuid,
            owner,
            name,
            comment,
            creation_time,
            modification_time,
            writable,
            in_use,
            # role,
            groups,
            # hosts,
            # ifaces,
            permissions,
            user_tags,
            # sources
        )

        return user


@dataclass
class Role:
    name: str

    @staticmethod
    def resolve_role(root: etree.Element) -> "Role":
        return Role(root.text)


@dataclass
class Observers:
    users: list
    groups: list
    # roles: list

    @staticmethod
    def resolve_observers(root: etree.Element, gmp) -> "Observers":
        if root is None:
            return None
        users = root.text
        if users is not None:
            users = users.split(' ')

        groups = Group.resolve_groups(root, gmp)
        # roles = Role.resolve_roles(root)

        observers = Observers(users, groups)

        return observers
