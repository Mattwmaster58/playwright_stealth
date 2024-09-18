from typing import Generic, Callable, TypeVar, overload
from typing_extensions import Concatenate, ParamSpec, Self

_T = TypeVar("_T")
_R_co = TypeVar("_R_co", covariant=True)
_R1_co = TypeVar("_R1_co", covariant=True)
_R2_co = TypeVar("_R2_co", covariant=True)
_P = ParamSpec("_P")


class class_or_instancemethod(classmethod[_T, _P, _R_co]):
    def __get__(
            self, instance: _T, type_: type[_T] | None = None
    ) -> Callable[_P, _R_co]:
        descr_get = super().__get__ if instance is None else self.__func__.__get__
        return descr_get(instance, type_)


class hybridmethod(Generic[_T, _P, _R1_co, _R2_co]):
    fclass: Callable[Concatenate[type[_T], _P], _R1_co]
    finstance: Callable[Concatenate[_T, _P], _R2_co] | None
    __doc__: str | None
    __isabstractmethod__: bool

    def __init__(
            self,
            fclass: Callable[Concatenate[type[_T], _P], _R1_co],
            finstance: Callable[Concatenate[_T, _P], _R2_co] | None = None,
            doc: str | None = None,
    ):
        self.fclass = fclass
        self.finstance = finstance
        self.__doc__ = doc or fclass.__doc__
        # support use on abstract base classes
        self.__isabstractmethod__ = bool(getattr(fclass, "__isabstractmethod__", False))

    def classmethod(self, fclass: Callable[Concatenate[type[_T], _P], _R1_co]) -> Self:
        return type(self)(fclass, self.finstance, None)

    def instancemethod(self, finstance: Callable[Concatenate[_T, _P], _R2_co]) -> Self:
        return type(self)(self.fclass, finstance, self.__doc__)

    @overload
    def __get__(self, instance: None, cls: type[_T]) -> Callable[_P, _R1_co]: ...

    @overload
    def __get__(self, instance: _T, cls: type[_T] | None = ...) -> Callable[_P, _R1_co] | Callable[_P, _R2_co]: ...

    def __get__(self, instance: _T, cls: type[_T] | None = None) -> Callable[_P, _R1_co] | Callable[_P, _R2_co]:
        if instance is None or self.finstance is None:
            # either bound to the class, or no instance method available
            return self.fclass.__get__(cls, None)
        return self.finstance.__get__(instance, cls)