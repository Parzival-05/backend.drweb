from functools import wraps
from typing import Any


def decorate_method(f, method: str):
    @wraps(f)
    def wrapper(meth):
        if meth.__name__ == method.lower():
            return f(meth)
        return meth

    return wrapper


def decorate_methods(**methods_decorated: list[Any]) -> list:
    method_decorators = []
    for method, decorators in methods_decorated.items():
        if not decorators:
            continue
        dec = None
        for _dec in decorators:
            dec = decorate_method(_dec(dec) if dec is not None else _dec, method)
            # decorators activation order is from bottom to top

        if dec is not None:
            method_decorators.append(dec)
    return method_decorators
