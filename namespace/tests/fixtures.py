"""
Jakub21, 2023Q1
Namespace package
"""

# from source.namespace import Namespace

fruits = {
  "banana": {
    "colors": [
      {"name": "yellow", "chance": 85}, {"name": "green", "chance": 15}
    ],
    "length": 23.1,
    "width": 6.5,
  },
  "apple": {
    "colors": [
      {"name": "red", "chance": 40}, {"name": "yellow", "chance": 25}, {"name": "green", "chance": 35}
    ],
    "length": 11.25,
    "width": 12.75,
  }
}


class Animal:
  LIMBS = [
    {"position": "front_left", "length": 25},
    {"position": "front_right", "length": 25},
    {"position": "back_left", "length": 25},
    {"position": "back_right", "length": 25},
  ]

  def __init__(self, species):
    self.eyes = 2
    self.tail = True
    self.species = species


def get_circular():
  a = {}
  b = {"a": a}
  a["b"] = b
  return a


serial_value = {
  "solar_system": {
    "star_name": "The Sun",
    "star_age": 4.6,
    "inner_planets": [
      {"name": "Mercury", "moons": 0},
      {"name": "Venus", "moons": 0},
      {"name": "Earth", "moons": 1},
      {"name": "Mars", "moons": 2},
    ]
  }
}


json_string = """
{
  "solar_system": {
    "star_name": "The Sun",
    "star_age": 4.6,
    "inner_planets": [
      {"name": "Mercury", "moons": 0},
      {"name": "Venus", "moons": 0},
      {"name": "Earth", "moons": 1},
      {"name": "Mars", "moons": 2}
    ]
  }
}
"""


yaml_string = """
solar_system:
  star_name: The Sun
  star_age: 4.6
  inner_planets:
    - name: Mercury
      moons: 0
    - name: Venus
      moons: 0
    - name: Earth
      moons: 1
    - name: Mars
      moons: 2
"""
