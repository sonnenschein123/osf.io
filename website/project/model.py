# -*- coding: utf-8 -*-
import logging
import re

from django.apps import apps

from modularodm import Q
from modularodm.exceptions import ValidationValueError

from website import settings
from website.util import sanitize

logger = logging.getLogger(__name__)


def has_anonymous_link(node, auth):
    """check if the node is anonymous to the user

    :param Node node: Node which the user wants to visit
    :param str link: any view-only link in the current url
    :return bool anonymous: Whether the node is anonymous to the user or not
    """
    if auth.private_link:
        return auth.private_link.anonymous
    return False


def validate_contributor(guid, contributors):
    OSFUser = apps.get_model('osf.OSFUser')
    user = OSFUser.load(guid)
    if not user or not user.is_claimed:
        raise ValidationValueError('User does not exist or is not active.')
    elif user not in contributors:
        raise ValidationValueError('Mentioned user is not a contributor.')
    return True

def get_valid_mentioned_users_guids(comment, contributors):
    """ Get a list of valid users that are mentioned in the comment content.

    :param Node comment: Node that has content and ever_mentioned
    :param list contributors: List of contributors on the node
    :return list new_mentions: List of valid users mentioned in the comment content
    """
    new_mentions = set(re.findall(r"\[[@|\+].*?\]\(htt[ps]{1,2}:\/\/[a-z\d:.]+?\/([a-z\d]{5})\/\)", comment.content))
    new_mentions = [
        m for m in new_mentions if
        m not in comment.ever_mentioned and
        validate_contributor(m, contributors)
    ]
    return new_mentions


def get_pointer_parent(pointer):
    """Given a `Pointer` object, return its parent node.
    """
    # The `parent_node` property of the `Pointer` schema refers to the parents
    # of the pointed-at `Node`, not the parents of the `Pointer`; use the
    # back-reference syntax to find the parents of the `Pointer`.
    parent_refs = pointer.node__parent
    assert len(parent_refs) == 1, 'Pointer must have exactly one parent.'
    return parent_refs[0]


def validate_category(value):
    """Validator for Node#category. Makes sure that the value is one of the
    categories defined in NODE_CATEGORY_MAP.
    """
    if value not in settings.NODE_CATEGORY_MAP.keys():
        raise ValidationValueError('Invalid value for category.')
    return True


def validate_title(value):
    """Validator for Node#title. Makes sure that the value exists and is not
    above 200 characters.
    """
    if value is None or not value.strip():
        raise ValidationValueError('Title cannot be blank.')

    value = sanitize.strip_html(value)

    if value is None or not value.strip():
        raise ValidationValueError('Invalid title.')

    if len(value) > 200:
        raise ValidationValueError('Title cannot exceed 200 characters.')

    return True


def validate_user(value):
    OSFUser = apps.get_model('osf.OSFUser')
    if value != {}:
        user_id = value.iterkeys().next()
        if OSFUser.find(Q('_id', 'eq', user_id)).count() != 1:
            raise ValidationValueError('User does not exist.')
    return True


class NodeUpdateError(Exception):
    def __init__(self, reason, key, *args, **kwargs):
        super(NodeUpdateError, self).__init__(reason, *args, **kwargs)
        self.key = key
        self.reason = reason


def validate_doi(value):
    if value and not re.match(r'\b(10\.\d{4,}(?:\.\d+)*/\S+(?:(?!["&\'<>])\S))\b', value):
        raise ValidationValueError('"{}" is not a valid DOI'.format(value))
    return True
