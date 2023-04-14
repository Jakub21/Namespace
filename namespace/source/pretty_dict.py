"""
Jakub21, 2023Q1
Namespace package
"""

from types import NoneType, FunctionType, MethodType, LambdaType
from datetime import datetime, date, time, timedelta
from re import match

TYPES = {
  "iterables": (list, tuple, set, bytes, bytearray),
}
ITER_MAX_LINE_WIDTH = 70


class PrettyDict(dict):

  def __init__(self, data):
    """
    Creates a pretty dictionary.
    """
    super().__init__(data)

  @staticmethod
  def _get_properties(data):
    """
    Converts anything to a dictionary. Builtin properties are omitted.
    """
    if isinstance(data, dict):
      return data
    return {name: getattr(data, name) for name in dir(data) if not match('__.*__', name)}

  # Overwrite default string methods

  def __repr__(self, *args, **kwargs):
    return self.to_str()

  # String composition

  def to_str(self, indent=2, _depth=0, _visited_containers=None, obj_name=''):
    _visited_containers = _visited_containers or []
    _visited_containers += [self]
    base_indent = ' ' * indent * _depth
    entry_indent = ' ' * indent * (_depth + 1)
    result = f'<{obj_name}> {{\n' if obj_name else f'{{\n'
    for key, val in self.items():
      val_str = self._convert_value(val, indent, _depth, _visited_containers)
      result += f'{entry_indent}{key}: {val_str}\n'
    result += f'{base_indent}}}'
    return result

  def _convert_value(self, value, indent=2, _depth=0, _visited_containers=None):
    _visited_containers = _visited_containers or []

    if value in _visited_containers:
      return '(...)'

    primitive_types = {
      (int, float, bool, NoneType): lambda val: str(val),
      (str,): lambda val: f'"{val}"',
      (type,): lambda val: f'<class {val.__name__}>',
      (datetime, date, time, timedelta): lambda val: f'<{type(val).__name__} {val}>',
      (dict,):
        lambda val: self._convert_dict(val, indent, _depth + 1, _visited_containers),
      TYPES["iterables"]:
        lambda val: self._convert_iterable(val, indent, _depth + 1, _visited_containers),
      (FunctionType, MethodType):
        lambda val: f'{val.__name__}()'
    }

    for types, callback in primitive_types.items():
      if not isinstance(value, types):
        continue
      return callback(value)

    return self._convert_object(value, indent, _depth, _visited_containers)

  def _convert_dict(self, data, indent=2, _depth=0, _visited_containers=None):
    _visited_containers = _visited_containers or []
    if not data:
      return 'dict (empty) { }'
    _visited_containers += [data]
    return self.__class__(self._get_properties(data)).to_str(indent, _depth, _visited_containers)

  def _convert_iterable(self, data, indent=2, _depth=0, _visited_containers=None):
    _visited_containers = _visited_containers or []
    SEPARATOR = ", "
    if not data:
      return f'{data.__class__.__name__} (empty)'

    elements = [
      elm.to_str(indent, _depth + 1, _visited_containers)
      if isinstance(elm, self.__class__)
      else self._convert_value(elm)
      for elm in data
    ]
    has_nested_structures = any([isinstance(x, (dict, TYPES["iterables"])) for x in data])

    # contain the iterable in one line it fits and there are no nested structures
    single_line = f'{data.__class__.__name__} [{SEPARATOR.join(elements)}]'
    if (len(single_line) + indent * _depth <= ITER_MAX_LINE_WIDTH) and not has_nested_structures:
      return single_line

    # contain the iterable in as few lines as possible if there are no nested structures
    if not has_nested_structures:
      result = f'{data.__class__.__name__} [\n{" " * indent * (_depth + 1)}'
      for idx, elm in enumerate(elements):
        len_after = len(result.split('\n')[-1] + SEPARATOR + elm)
        if len_after > ITER_MAX_LINE_WIDTH:
          result += SEPARATOR + '\n' + ' ' * (indent * (_depth + 1))
        elif idx:
          result += SEPARATOR
        result += elm
      return result + '\n' + ' ' * (indent * _depth) + ']'

    # each element in new line for best representation of nested structures
    result = f'{data.__class__.__name__} [\n'
    for elm in elements:
      result += f'{" " * indent * (_depth + 1)}- {elm.strip()}\n'
    return result + ' ' * (indent * _depth) + ']'

  def _convert_object(self, data, indent=2, _depth=0, _visited_containers=None):
    _visited_containers = _visited_containers or []
    _visited_containers += [data]
    ns = self.__class__(self._get_properties(data))
    return ns.to_str(indent, _depth + 1, _visited_containers, data.__class__.__name__)
