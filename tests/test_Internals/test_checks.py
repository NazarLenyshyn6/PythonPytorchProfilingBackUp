import pytest
from Internals.checks import ValidateType
from contextlib import nullcontext
from Internals.exceptions import InvalidInputTypeError, MissingArgumentError
from types import FunctionType, BuiltinFunctionType


@pytest.mark.parametrize('expected, func, kwargs, raised_exception',
                         [
                             (('x', int), lambda x: 1, {'x': 1}, nullcontext()),
                             ([('x', int), ('y', str)], lambda x, y: 1, {'x': 1, 'y': '1'}, nullcontext()),
                             (('x', int), lambda x: 1, {'x': 'hello'}, pytest.raises(InvalidInputTypeError)),
                             (('x', int), lambda x: 1, {}, pytest.raises(MissingArgumentError)),
                             ([('x', int), ('y', str)], lambda x, y: 1, {'x': 1}, pytest.raises(MissingArgumentError)),
                         ])
def test_ValidateType(expected, func, kwargs, raised_exception):
    with raised_exception:
        ValidateType(expected)(func)(**kwargs)
