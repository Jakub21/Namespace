# Namespace

New dict-like data structure.
- Enabled access of elements with both attribute syntax and dictionary syntax.
- Provides methods for loading and dumping into serial formats.
- Easy way for pretty printing of complex structures.

## Installation & usage

[Newest version]([url](https://pypi.org/project/j-namespace/)) can be installed with
```
pip install j-namespace
```

[Legacy versions]([url](https://pypi.org/project/javascript-namespaces/)) are kept here for backwards compatibility
```
pip install javascript-namespaces
```

### Simple usage example

```python
from namespace import Namespace

# these two create the same object
ns1 = Namespace(bananas = 5, apples = 10)
ns2 = Namespace.Dict({"bananas": 5, "apples": 10})

# both syntax styles are supported, the same is true for assignments
print(ns1.bananas) # -> 5
print(ns1["apples"]) # -> 10

```

> **NOTE** Uppercase methods always return a Namespace instance

### Recursive namespaces and pretty print

Some structures are too complex to be readable when dumped to a string.
Recursive method converts all mappings (dicts, objects, etc.) to a namespace instance.
Below is an example of how it looks like when printed.

```python
from namespace import Namespace

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

ns = Namespace.Recursive(fruits)
print(ns)
```

Output

```
{
  banana: {
    colors: list [
      - {
        name: "yellow"
        chance: 85
      }
      - {
        name: "green"
        chance: 15
      }
    ]
    length: 23.1
    width: 6.5
  }
  apple: {
    colors: list [
      - {
        name: "red"
        chance: 40
      }
      - {
        name: "yellow"
        chance: 25
      }
      - {
        name: "green"
        chance: 35
      }
    ]
    length: 11.25
    width: 12.75
  }
}
```

`Recursive` factory also works with objects

```python
from namespace import Namespace

class Bar:
  CLS_ATTR = 'class attribute'

  def __init__(self, a):
    self.a = a

  def do_stuff(self):
    pass

bar = Bar(1)

ns = Namespace.Recursive(bar)
print(ns)
```

Output

```
{
  CLS_ATTR: "class attribute"
  a: 1
  do_stuff: do_stuff()
}
```


When an iterable does not contain nested structures but only primitive data - it is not unpacked.
Other iterable types (tuples, set, etc.) are represented in the same way.
The only way to tell the difference is by the type displayed before its content.

```python
from namespace import Namespace

numbers = {
  "lots_of_numbers": [n for n in range(100)],
  "my_tuple": (1, "foo"),
  "my_set": {2, "bar"},
}

ns = Namespace.Dict(numbers)
print(ns)
```

Output

```
{
  lots_of_numbers: list [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
    19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
    36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
    53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
    70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
    87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99
  ]
  my_tuple: tuple [1, "foo"]
  my_set: set ["bar", 2]
}
```
