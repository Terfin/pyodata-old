from edmtypes import *
from pdb import Pdb

debug = Pdb()

class EntityBase(type):
	def __init__(cls, clsname, bases, _dict):
		setattr(cls, '__odata__', _dict)
		for key in _dict:

			if hasattr(_dict[key], '__edmtype__'):
				setattr(cls, "".join(['_', key]), None)
				fget = _create_fget(key)
				fset = _create_fset(key)
				setattr(cls, key, property(fget, fset))
		return type.__init__(cls, clsname, bases, _dict)


def _create_fget(k):
	return lambda self: getattr(self, "".join(['_', k]))

def _create_fset(k):
	return lambda self, value: setattr(self, "".join(['_', k]), value)

def entity_base():
	return EntityBase("Base", (object, ), {})


class Foo(entity_base()):
	a = String('Foobar')

d = Foo()
print d.a