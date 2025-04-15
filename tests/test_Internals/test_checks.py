"""Tests for checks module."""

import pytest
from types import FunctionType, BuiltinFunctionType

import contextlib

from Internals import checks
from Internals import exceptions


@pytest.mark.parametrize(
    'expected, func, kwargs, raised_exception',
    [
        (('x', int), lambda x: 1, {'x': 1}, contextlib.nullcontext()),
        ([('x', int), ('y', str)], lambda x, y: 1, {'x': 1, 'y': '1'}, contextlib.nullcontext()),
        (('x', int), lambda x: 1, {'x': 'hello'}, pytest.raises(exceptions.InvalidInputTypeError)),
        (('x', int), lambda x: 1, {}, pytest.raises(exceptions.MissingArgumentError)),
        ([('x', int), ('y', str)], lambda x, y: 1, {'x': 1}, pytest.raises(exceptions.MissingArgumentError)),
        ]
    )
def test_ValidateType(
    expected, 
    func, 
    kwargs, 
    raised_exception
    ):
    with raised_exception:
        checks.ValidateType(expected)(func)(**kwargs)
