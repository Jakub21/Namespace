
class Namespace:
  '''Converts dictionaries to namespaces'''
  def __init__(self, **data):
    self.__dict__.update(data)

  @classmethod
  def fromDict(cls, input_dict):
    obj = cls.__new__(cls)
    obj.__dict__.update(input_dict)
    return obj

  @classmethod
  def recursive(cls, **data):
    obj = cls.__new__(cls)
    for k, v in data.items():
      if type(v) is dict:
        v = cls.recursive(v)
      obj.__dict__.update({k:v})
    return obj

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

  def __str__(self, indent=0, className='Namespace', onlyHeadObjs=[]):
    indentWidth = 2
    self.__onlyHeadObjs__ = onlyHeadObjs + [self]
    self.__repr_indent__ = indent
    result = className + ' {\n'
    def convertPrimitive(x):
      if type(x) == str:
        x = '"'+x+'"'
      return str(x)
    def convertDict(x):
      return Namespace(**x).__str__(self.__repr_indent__+1, 'dict',
        self.__onlyHeadObjs__)
    def convertList(x):
      if len(x) == 0: return '[]'
      else:
        self.__repr_indent__ += 1
        r = '['
        for xx in x:
          r += '\n' + ' '*indentWidth*(self.__repr_indent__+1) + str(choice(xx))
        r += '\n'+' '*indentWidth*self.__repr_indent__+']\n'
        self.__repr_indent__ -= 1
        return r
    def convertObject(x):
      if x in self.__onlyHeadObjs__: return self.getObjectHead(x)
      self.__onlyHeadObjs__ += [x]
      return Namespace(**x.__dict__).__str__(self.__repr_indent__+1,
        self.getObjectHead(x), self.__onlyHeadObjs__)
    def convertClass(x):
      return f'<class {x.__name__}>'
    def choice(x):
      if type(x) in [int, str, float, bool]:
        return convertPrimitive(x)
      elif type(x) == dict:
        return convertDict(x)
      elif type(x) == list:
        return convertList(x)
      elif 'object at' in str(x):
        return convertObject(x)
      elif type(x) == type(list): # class (not instance)
        return convertClass(x)
    for k, v in self.__dict__.items():
      if k in ['__repr_indent__', '__onlyHeadObjs__']: continue
      result += ' '*indentWidth*(self.__repr_indent__+1) + f'{k}: {choice(v)}\n'
    result += ' '*indentWidth*self.__repr_indent__ + '}'
    del self.__repr_indent__
    del self.__onlyHeadObjs__
    return result

  def __repr__(self, *args, **kwargs):
    return self.__str__(*args, **kwargs)

  @staticmethod
  def getObjectHead(obj):
    name = obj.__class__.__name__
    hexId = '0x' + hex(id(obj))[2:].upper()
    return f'<{name} at {hexId}>'

  @classmethod
  def getObjectStructure(cls, obj):
    ns = Namespace(**obj.__dict__)
    return ns.__str__(0, cls.getObjectHead(obj), [obj])
