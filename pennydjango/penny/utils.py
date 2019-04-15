import bleach
import re
import uuid

from enum import Enum

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import (DecimalField, CharField, IntegerField,
                              AutoField, QuerySet)

from penny.collect_fields import get_fields


def sanitize_html(text, strip=False, allow_safe=True):
    """
    Strip/escape html tags, attributes, and styles using a whitelist.
    Set allow_safe=False to escape all html tags, by default it allows
    a limited subset of safe ones (e.g. <b>, <i>, <img>...).
    """
    attrs = {
        '*': [
            'style', 'href', 'alt', 'title', 'class',
            'border', 'padding', 'margin', 'line-height'
        ],
        'img': ['src'],
    }
    if not allow_safe:
        tags = []
        styles = []
    else:
        tags = [
            'p', 'b', 'br', 'em', 'blockquote', 'strong', 'i', 'u',
            'a', 'ul', 'li', 'ol', 'img', 'span', 'h1', 'h2', 'h3',
            'h4', 'h5', 'h6', 'h7', 'table', 'td', 'thead', 'tbody',
            'tr', 'div', 'sub', 'sup', 'small'
        ]
        styles = [
            'color', 'font-weight', 'font-size', 'font-family',
            'text-decoration', 'font-variant'
        ]

    cleaned_text = bleach.clean(text, tags, attrs, styles, strip=strip)

    return cleaned_text  # "free of XSS"


def get_short_uuid(uuid) -> str:
    """get the first block of a 4-word UUID to use as a short identifier"""
    full_uuid = str(uuid)
    return full_uuid.split('-', 1)[0]


class StrBasedEnum(Enum):
    @classmethod
    def from_str(cls, string: str):
        return cls._member_map_[string.upper()]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class ExtendedEncoder(DjangoJSONEncoder):
    """
    Extended json serializer that supports serializing several model
    fields and objects
    """

    def default(self, obj):
        cls_name = obj.__class__.__name__

        if isinstance(obj, (DecimalField, CharField)):
            return str(obj)

        elif isinstance(obj, (IntegerField, AutoField)):
            return int(obj)

        elif cls_name in ('Action', 'Event'):
            return obj.name

        elif hasattr(obj, '__json__'):
            return obj.__json__()

        elif isinstance(obj, QuerySet):
            return list(obj)

        elif isinstance(obj, uuid.UUID):
            return str(obj)

        elif isinstance(obj, bytes):
            return obj.decode()

        elif cls_name == 'CallableBool':
            # ^ shouldn't check using isinstance because CallableBools
            #   will eventually be deprecated
            return bool(obj)

        elif cls_name == 'AnonymousUser':
            # ^ cant check using isinstance since models aren't ready
            #   yet when this is called
            return None  # AnonUser should always be represented as null in JS

        elif isinstance(obj, StrBasedEnum):
            return str(obj)

        elif cls_name in ('dict_items', 'dict_keys', 'dict_values'):
            return tuple(obj)

        return DjangoJSONEncoder.default(self, obj)

    @classmethod
    def convert_for_json(cls, obj, recursive=True):
        if recursive:
            if isinstance(obj, dict):
                return {
                    cls.convert_for_json(k): cls.convert_for_json(v)
                    for k, v in obj.items()
                }
            elif isinstance(obj, (list, tuple)):
                return [cls.convert_for_json(i) for i in obj]

        try:
            return cls.convert_for_json(cls().default(obj))
        except TypeError:
            return obj


def convert_to_snake(name):
    """
    Converts camelCase string to snake_case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_output_fields(info):
    """
    return the requested output fields as a list
    """
    fields_dict = get_fields(info)["edges"]["node"]
    fields = [convert_to_snake(key)
              for key in fields_dict
              if key not in ['cursor']]
    return fields
