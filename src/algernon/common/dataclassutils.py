"""
Class maps for deserializing JSON data from the database into its proper instance.
"""
import dataclasses
from enum import EnumMeta
from typing import Dict, Any, Optional


def dataclass_to_dict(dc: Any) -> Dict:
    if hasattr(dc, 'to_dict'):
        return dc.to_dict()
    d = dataclasses.asdict(dc)
    d['_type_'] = dc.__class__.__name__
    return d


def dataclass_deserialize_enums(dc_class: Any, d: Dict):
    """
    Deserializes Enums in a dict of a dataclass.

    Our json_deserializer stores enums as their FQN, e.g. 'JobState.new'. This helper creates an instance of the
    respective enum member.

    :param dc_class: The class of the dataclass
    :param d: The dict
    :raises ValueError: If found value is not a member of that enum
    """
    for f in dataclasses.fields(dc_class):
        if isinstance(f.type, EnumMeta):
            enum_cls, enum_val = d[f.name].split('.')
            d[f.name] = f.type(enum_val)
