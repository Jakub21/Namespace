"""
Jakub21, 2023Q1
Namespace package
"""

from source import Namespace
from .fixtures import Animal, fruits, get_circular, serial_value, json_string, yaml_string


# constructors


def test_constructor():
  ns = Namespace(fruits)
  assert isinstance(ns, Namespace)
  assert not isinstance(ns.banana, Namespace) and isinstance(ns.banana, dict)
  assert not isinstance(ns.banana["colors"][0], Namespace) and isinstance(ns.banana["colors"][0], dict)


def test_kwargs_factory():
  ns = Namespace.Kwargs(apples = 5, bananas = 4, berries = 32)
  assert ns.apples == 5
  assert ns["bananas"] == 4
  assert ns.get("berries") == 32


def test_recursive_factory_with_dict():
  ns = Namespace.Recursive(fruits)
  assert isinstance(ns, Namespace)
  assert isinstance(ns.banana, Namespace)
  assert isinstance(ns.banana.colors[0], Namespace)


def test_recursive_factory_with_circular_dict():
  # only test if it throws no errors
  ns = Namespace.Recursive(get_circular())


# object attribute & dict indexing syntax


def test_getters_are_synonymous():
  ns = Namespace(fruits)
  with_index = ns["banana"]
  with_getattr = getattr(ns, "banana")
  with_get = ns.get("banana")
  with_dot = ns.banana

  assert with_index is with_getattr
  assert with_getattr is with_get
  assert with_get is with_dot


def test_setters_are_synonymous():
  value = "UniqueValue"
  ns_index = Namespace(fruits)
  ns_index["unique"] = value

  ns_setattr = Namespace(fruits)
  setattr(ns_setattr, "unique", value)

  ns_dot = Namespace(fruits)
  ns_dot.unique = value

  assert ns_index.unique is ns_setattr.unique
  assert ns_setattr.unique is ns_dot.unique


# loading from serial data formats


# def test_from_json():
#   ns = Namespace.FromJSON(json_string)
#   assert ns.__dict__ == serial_value
#   # serial_value, json_string, yaml_string
