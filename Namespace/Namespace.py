SPACES = 2

class Namespace:
  '''Converts dictionaries to namespaces'''
  def __init__(self, **data):
    self.__dict__.update(data)

  # Implement dictionary interface methods

  def __getitem__(self, key):
    return self.__dict__[key]

  def __setitem__(self, key, value):
    self.__dict__[key] = value

  def items(self):
    return self.__dict__.items()

  def keys(self):
    return self.__dict__.keys()

  def values(self):
    return self.__dict__.values()

  def __repr__(self, *args, **kwargs):
    return self.toStr(*args, **kwargs)

  def __str__(self, *args, **kwargs):
    return self.toStr(*args, **kwargs)

  def toStr(self, className=None, maxDepth=-1, depth=0, extendedObjs=[]):
    extendedObjs += [self]
    if className is None: className = self.__strGetObjectHead(self)
    result = className + ' {\n'

    for item in self.__dict__.values():
      if isinstance(item.__class__, type) or type(item) == dict:
        extendedObjs += [item]

    indent = ' ' * SPACES * depth
    for key, val in self.__dict__.items():
      try: val = self.__strConvert(val, depth, maxDepth, extendedObjs)
      except Exception as e:
        print(' > ', end=key)
        if depth == 0: print('\n[PARTIAL RESULT]', result)
        raise e.with_traceback(None)
      result += f'{indent}{" "*SPACES}{key}: {val}\n'
    result += indent + '}'
    return result

  @classmethod
  def __strConvert(cls, item, depth, maxDepth, extendedObjs):
    # Primitive types
    if type(item) in [str, int, float, bool, type(None)]: return cls.__strCvtPrimitive(item)
    # Class
    elif isinstance(item, type): return cls.__strCvtClass(item)
    # Dictionary
    elif type(item) is dict: return cls.__strCvtDict(item, depth, maxDepth, extendedObjs)
    # Iterables
    elif type(item) is list:
      return cls.__strCvtIterable(item, depth, maxDepth, 'list', '[]', extendedObjs)
    elif type(item) is tuple:
      return cls.__strCvtIterable(item, depth, maxDepth, 'tuple', '()', extendedObjs)
    elif type(item) is set:
      return cls.__strCvtIterable(item, depth, maxDepth, 'set', '{}', extendedObjs)
    # Object
    elif isinstance(item.__class__, type):
      return cls.__strCvtObject(item, depth, maxDepth, extendedObjs)

  @staticmethod
  def __strCvtPrimitive(item):
    if type(item) == str: item = f'"{item}"'
    return str(item)

  @staticmethod
  def __strCvtClass(item):
    return f'<class {item.__name__}>'

  @staticmethod
  def __strCvtDict(item, depth, maxDepth, extendedObjs):
    length = len(item)
    # head only
    if not length: return 'dict (empty) { }'
    if depth >= maxDepth and maxDepth != -1: return f'dict ({length})' + ' { ... }'
    # head + content
    return Namespace(**item).toStr('dict', maxDepth, depth+1, extendedObjs)

  @classmethod
  def __strCvtIterable(cls, item, depth, maxDepth, name, limiters, extendedObjs):
    open, close = limiters
    length = len(item)
    # head only
    if not length: return f'{name} (empty) {open} {close}'
    if depth >= maxDepth and maxDepth != -1: return f'{name} ({length}) {open} ... {close}'
    # head + content
    result = f'{name} ({length}) {open}'
    indent = ' ' * SPACES * (depth + 1)
    elmIndent = ' ' * SPACES * (depth + 2)
    for elm in item:
      elm = cls.__strConvert(elm, depth+1, maxDepth, extendedObjs)
      extendedObjs += [elm]
      result += f'\n{elmIndent}- {elm},'
    return f'{result}\n{indent}{close}'

  @classmethod
  def __strCvtObject(cls, item, depth, maxDepth, extendedObjs):
    head = cls.__strGetObjectHead(item)
    # content unaccessible
    try: item.__dict__
    except AttributeError:
      return head + ' (inaccessible)'
    # head only
    if (depth >= maxDepth and maxDepth != -1) or item in extendedObjs:
      return head + f' {{ {len(item.__dict__)} attributes }}'
    if len(item.__dict__) == 0:
      return head + ' (empty)'
    # head + content
    ns = Namespace(**item.__dict__)
    return ns.toStr(head, maxDepth, depth+1, extendedObjs)

  @staticmethod
  def __strGetObjectHead(item):
    return f'<{item.__class__.__name__} at {"0x" + hex(id(item))[2:].upper()}>'

  @classmethod
  def getObjectStructure(cls, item, maxDepth=-1):
    try: item.__dict__
    except AttributeError: raise AttributeError('Can not access content of this object')
    return Namespace(**item.__dict__).toStr(cls.__strGetObjectHead(item), maxDepth, 0, [item])
