import datetime
from typing import List
from dataclasses import dataclass
from lxml import etree
from gvm.protocols.base import GvmProtocol

# from gvm.protocols.gmp import Gmp

from .utils import (
    get_bool_from_element,
    get_int_from_element,
    get_text_from_element,
    get_datetime_from_element,
)


@dataclass
class Owner:
    """
    Arguments:
        name: The name of the owner.
    """

    name: str

    @staticmethod
    def resolve_owner(root: etree.Element) -> "Owner":
        """ Resolve information of a owner.

        :param root: owner XML element from GMP.
        """
        if root is None:
            return None
        name = root.find('name').text
        if name is None:
            return None
        else:
            return Owner(name)


@dataclass
class Tag:
    """Information on a single tag.

    Arguments:
        uuid: uuid of the tag (omitted when using names_only).
        name: Name of the tag (usually namespace:predicate).
        value: Value associated with the tag.
        comment: Comment for the tag.
    """

    uuid: str
    name: str
    value: str
    comment: str

    @staticmethod
    def resolve_tags(root: etree.Element) -> list:
        """ Resolve a list of tags.
        If there is just one tag, it returns the Tag.

        :param root: XML element from GMP with a list of tag elements.
        """
        if root is None:
            return None

        tags = []
        for child in root:
            if child.tag == "tag":
                tags.append(Tag.resolve_tag(child))

        if len(tags) == 1:
            return tags[0]

        return tags

    @staticmethod
    def resolve_tag(root: etree.Element) -> "Tag":
        """ Resolve information of a single tag.

        :param root: tag XML element from GMP.
        """
        if root is None:
            return None

        uuid = root.get("id")
        name = get_text_from_element(root, "name")
        value = get_text_from_element(root, "value")
        comment = get_text_from_element(root, "comment")

        return Tag(uuid, name, value, comment)


@dataclass
class UserTags:
    """
    Arguments:
        count: Number of attached tags.
        tags: attached tags
    """

    count: int
    tags: List[Tag]

    @staticmethod
    def resolve_user_tags(root: etree.Element) -> "UserTags":
        """ resolve information of user tags

        :param root: user_tags XML element from GMP.
        """
        count = get_int_from_element(root, "count")
        tags = Tag.resolve_tags(root)

        if count is None and tags is None:
            return None

        return UserTags(count, tags)


@dataclass
class Permission:
    """ Permissions that the current user has.

    Arguments:
        name: The name of the permission.
    """

    name: str

    @staticmethod
    def resolve_permissions(root: etree.Element) -> list:
        """ Resolve a list of permissions.
        If there is just one Permission it returns the Permission.

        :param root: permissions XML element from GMP.
        """
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
    """
    Arguments:
        gmp: Gmp Object for automatical reloading of information.
        uuid: uuid of the group.
        owner: Owner of the group.
        name: The name of the group.
        comment: The comment on the group.
        creation_time: Date and time the group was created.
        modification_time: Date and time the group was last modified.
        writable: Whether the group is writable.
        in_use: Whether the group is in use.
        permissions: Permissions that the current user has on the group.
        user_tags: Tags attached to the group.
        users: List of the users in the group.
    """

    gmp: GvmProtocol = None
    uuid: str = None
    owner: Owner = None
    name: str = None
    comment: str = None
    creation_time: datetime.datetime = None
    modification_time: datetime.datetime = None
    writable: bool = None
    in_use: bool = None
    permissions: list = None
    user_tags: UserTags = None
    users: list = None

    @staticmethod
    def resolve_groups(root: etree.Element, gmp):
        """ Resolve a list of groups.
        If there is just one group.

        :param root: XML element from GMP with a list of group elements.
        """
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
        """ Resolve information of a group.

        :param root: group XML element from GMP.
        """
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
    """
    Arguments:
        uuid: ID of user.
        owner: Owner of the user.
        name: The name of the user.
        comment: The comment on the user.
        creation_time: Creation time of the user.
        modification_time: Last time the user was modified.
        writable: Whether the user is writable.
        in_use: Whether this user is currently in use.
        groups: The groups the user belongs to.
        permissions: Permissions that the current user has on the user.
        user_tags: Tags attached to the user.
    """

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
    permissions: List[Permission]
    user_tags: UserTags
    # sources

    @staticmethod
    def resolve_users(root: etree.Element, gmp) -> list:
        """ Resolve a list of users.

        :param root: XML element from GMP with a list of users.
        """
        if root is None:
            return None

        users = []

        for child in root:
            if child.tag == "user":
                users.append(User.resolve_user(child, gmp))

        return users

    @staticmethod
    def resolve_user(root: etree.Element, gmp) -> "User":
        """ Resolve information of a single user.

        :param root: user XML element from GMP.
        """
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
    """
    Arguments:
        name: Name of the role.
    """

    name: str

    @staticmethod
    def resolve_role(root: etree.Element) -> "Role":
        """ Resolve information of a role.

        :param root: role XML element from GMP.
        """
        return Role(root.text)


@dataclass
class Observers:
    """
    Arguments:
        users: Users allowed to observe the task.
        groups: Group allowed to observe the task.
    """

    users: list
    groups: list
    # roles: list

    @staticmethod
    def resolve_observers(root: etree.Element, gmp) -> "Observers":
        """ Resolve a list of observers.

        :param root: observers XML element from GMP.
        """
        if root is None:
            return None
        users = root.text
        if users is not None:
            users = users.split(' ')

        groups = Group.resolve_groups(root, gmp)
        # roles = Role.resolve_roles(root)

        observers = Observers(users, groups)

        return observers
