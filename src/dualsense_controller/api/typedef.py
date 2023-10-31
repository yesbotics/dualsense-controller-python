from typing import Callable, TypeVar

PropertyType = TypeVar('PropertyType')
_PrChCb0 = Callable[[], None]
_PrChCb1 = Callable[[PropertyType], None]
_PrChCb2 = Callable[[PropertyType, int], None]
_PrChCb3 = Callable[[PropertyType, PropertyType, int], None]
PropertyChangeCallback = _PrChCb0 | _PrChCb0 | _PrChCb2 | _PrChCb3
