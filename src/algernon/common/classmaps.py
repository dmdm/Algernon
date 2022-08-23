from typing import Dict, Any, Optional

from algernon.common.models import FetchUrlPayload

DATACLASS_MAP = {
    'NewUrlPayload': FetchUrlPayload,
}


def dataclass_from_dict(d: Dict,  dc_map: Optional[Dict] = None) -> Any:
    # Cannot put this function in 'dataclassutils', that would create circular dependency:
    # dataclassutils imports DATACLASS_MAP that imports JobStatePayload that imports dataclassutils
    if not dc_map:
        dc_map = DATACLASS_MAP
    clazz = dc_map.get(d['_type_'])
    if not clazz:
        raise KeyError(f'''Failed to create dataclass from dict: no class for type "{d['_type_']}"''')
    del d['_type_']
    if hasattr(clazz, 'from_dict'):
        return clazz.from_dict(d)
    return clazz(**d)
