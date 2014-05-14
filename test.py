from service.servicecore import *
from edm.edmtypes import *
from edm.core import *
from pdb import Pdb

debug = Pdb()


@servicemember
class Foo(entity_base()):
	key = 'foo'
	__ename__ = 'MyFoo'
	a = String("foo")

debug.set_trace()