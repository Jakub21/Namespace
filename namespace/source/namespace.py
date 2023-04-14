"""
Jakub21, 2023Q1
Namespace package
"""

import json
import yaml

from .pretty_dict import PrettyDict, TYPES


class Namespace(PrettyDict):
  """
  Unified data format.
  Enabled access of elements with both attribute syntax and dictionary syntax.
  Provides methods for loading and dumping into serial formats.
  Easy way for pretty printing of complex structures.
  """

  def __init__(self, data):
    """
    Creates a namespace from a dictionary.
    """
    super().__init__(data)

  # alternative constructors

  @classmethod
  def Kwargs(cls, **kwargs):
    """
    Creates a flat namespace with all keyword arguments as elements.
    """
    return cls(kwargs)

  @classmethod
  def Recursive(cls, data, _parents=None):
    """
    Creates a namespace with recursive traversing. This means that nested dictionaries and objects
    will also be converted to a namespace. Including the ones that are inside iterables.
    Input can be either an object or a dictionary.
    """
    obj = cls.__new__(cls)

    _parents = _parents or []
    _parents += [{"entry": data, "ns": obj}]
    properties = cls._get_properties(data)

    def convert(elm):
      for parent in _parents:
        if parent["entry"] is elm:
          return parent["ns"]
      return cls.Recursive(elm, _parents) if isinstance(elm, dict) else elm

    for key, val in properties.items():
      if isinstance(val, TYPES["iterables"]):
        properties[key] = []
        for entry in val:
          properties[key] += [convert(entry)]
        properties[key] = type(val)(properties[key])
        continue
      properties[key] = convert(val)
    obj.__init__(properties)
    return obj

  # object attribute syntax support

  def __getattr__(self, item):
    return self[item]

  def __setattr__(self, key, value):
    self[key] = value

  # loading from serial data formats

  @classmethod
  def FromJSON(cls, data):
    """
    Parses a JSON string and creates a namespace with all elements from the resulting dictionary
    (with recursive traversing)
    """
    return cls.Recursive(json.loads(data))

  @classmethod
  def FromJSONFile(cls, path):
    """
    Parses content from a JSON file and creates a namespace with all elements from the resulting dictionary
    (with recursive traversing)
    """
    with open(path, 'r') as file:
      return cls.FromJson(file.read())

  @classmethod
  def FromYAML(cls, data, loader=None):
    """
    Parses a JSON string and creates a namespace with all elements from the resulting dictionary
    (with recursive traversing)
    """
    return cls.Recursive(yaml.load(data, loader or yaml.SafeLoader))

  @classmethod
  def FromYAMLFile(cls, path):
    """
    Parses content from a JSON file and creates a namespace with all elements from the resulting dictionary
    (with recursive traversing)
    """
    with open(path, 'r') as file:
      return cls.FromYAML(file.read())

  # dumping into serial data formats

  def _serialize(self):
    """
    Traverses the whole structure and returns a dict that can be fed to various serializers.
    """
    raise NotImplementedError

  def to_json(self):
    """
    Converts the entire namespace to a JSON string.
    """
    raise NotImplementedError

  def to_json_file(self, path):
    """
    Converts the entire namespace to a JSON string.
    """
    with open(path, 'w') as file:
      file.write(self.to_json())

  def to_yaml(self):
    """
    Converts the entire namespace to a YAML string.
    """
    raise NotImplementedError

  def to_yaml_file(self, path):
    """
    Converts the entire namespace to a YAML string.
    """
    with open(path, 'w') as file:
      file.write(self.to_yaml())
