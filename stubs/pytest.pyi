from typing import ContextManager, Any, Optional, Type


def raises(exc: Optional[Type[Exception]] = None) -> ContextManager[Any]:
    ...
