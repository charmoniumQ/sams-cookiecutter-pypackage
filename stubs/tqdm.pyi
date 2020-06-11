import sys
import contextlib
from types import TracebackType
from typing import (
    TypeVar,
    Generic,
    Iterable,
    IO,
    Union,
    ContextManager,
    Optional,
    Any,
    Type,
    Iterator,
    Dict,
    Callable,
)
from contextlib import contextmanager

Value = TypeVar("Value")

class tqdm(Generic[Value]):
    def __init__(
        self,
        iterable: Optional[Iterable[Value]] = None,
        desc: Optional[str] = None,
        total: Optional[int] = None,
        leave: Optional[bool] = True,
        file: IO[str] = sys.stderr,
        ncols: Optional[int] = None,
        mininterval: Optional[float] = 0.1,
        maxinterval: Optional[float] = 10.0,
        miniters: Optional[int] = None,
        ascii: Optional[bool] = None,
        disable: Optional[bool] = False,
        unit: Optional[str] = "it",
        unit_scale: Optional[Union[bool, float, int]] = False,
        dynamic_ncols: Optional[bool] = False,
        smoothing: Optional[float] = 0.3,
        bar_format: Optional[str] = None,
        initial: Optional[int] = 0,
        position: Optional[int] = None,
        postfix: Optional[Dict[str, Any]] = None,
        unit_divisor: Optional[int] = 1000,
        write_bytes: Optional[bool] = None,
        gui: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def __iter__(self) -> Iterator[Value]: ...
    def tqdm(
        self,
        iterable: Optional[Iterable[Value]] = None,
        desc: Optional[str] = None,
        total: Optional[int] = None,
        leave: Optional[bool] = True,
        file: IO[str] = sys.stderr,
        ncols: Optional[int] = None,
        mininterval: Optional[float] = 0.1,
        maxinterval: Optional[float] = 10.0,
        miniters: Optional[int] = None,
        ascii: Optional[bool] = None,
        disable: Optional[bool] = False,
        unit: Optional[str] = "it",
        unit_scale: Optional[Union[bool, float, int]] = False,
        dynamic_ncols: Optional[bool] = False,
        smoothing: Optional[float] = 0.3,
        bar_format: Optional[str] = None,
        initial: Optional[int] = 0,
        position: Optional[int] = None,
        postfix: Optional[Dict[str, Any]] = None,
        unit_divisor: Optional[int] = 1000,
        write_bytes: Optional[bool] = None,
        gui: bool = False,
        **kwargs: Any,
    ) -> Iterable[Value]: ...
    # ) -> tqdm[Value]: ...
    def update(self, n: int = 1) -> None: ...
    def close(self) -> None: ...
    def clear(self, nolock: bool = False) -> None: ...
    def refresh(self, nolock: bool = False) -> None: ...
    def unpause(self) -> None: ...
    def reset(self, total: Optional[int] = None) -> None: ...
    def set_description(
        self, desc: Optional[bool] = None, refresh: bool = True
    ) -> None: ...
    def set_description_str(
        self, desc: Optional[bool] = None, refresh: bool = True
    ) -> None: ...
    def set_postfix(
        self,
        ordered_dict: Optional[Dict[str, Any]] = None,
        refresh: bool = True,
        **kwargs: Any,
    ) -> None: ...
    def set_postfix_str(
        self,
        ordered_dict: Optional[Dict[str, Any]] = None,
        refresh: bool = True,
        **kwargs: Any,
    ) -> None: ...
    @classmethod
    def write(
        cls,
        s: Any,
        file: Optional[IO[str]] = None,
        end: str = "\n",
        nolock: bool = False,
    ) -> None: ...
    def get_lock(self) -> None: ...
    def set_lock(self) -> Lock: ...
    def display(self, msg: Optional[str] = None, pos: Optional[int] = None) -> None: ...
    @staticmethod
    def status_printer(file: IO[str]) -> Callable[[str], None]: ...
    @classmethod
    def external_write_mode(
        cls, file: Optional[IO[str]] = None, nolock: bool = False
    ) -> ContextManager[None]: ...
    @staticmethod
    def format_interval(t: int) -> str: ...
    @staticmethod
    def format_meter(
        n: int,
        total: int,
        elapsed: float,
        ncols: Optional[int] = None,
        prefix: str = "",
        ascii: Optional[Union[bool, str]] = False,
        unit: str = "it",
        unit_scale: bool = False,
        rate: Optional[float] = None,
        bar_format: Optional[str] = None,
        postfix: Optional[Union[Dict[str, Any], str]] = None,
        unit_divisor: int = 1000,
        **extra_kwargs: Any,
    ) -> str: ...
    @staticmethod
    def format_num(n: int) -> str: ...
    @staticmethod
    def format_sizeof(num: int, suffix: str = "", divisor: int = 1000) -> str: ...

class Lock:
    def __init__(self) -> None: ...
    def acquire(self) -> None: ...
    def release(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool: ...
