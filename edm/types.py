from abc import ABCMeta, abstractproperty, abstractmethod
from pdb import Pdb
from lxml import etree as ET
from lxml import objectify

debugger = Pdb()

class UnknownFacetError(AttributeError):
	pass

class EDMElement(type):
	def __init__(cls, clsname, bases, _dict):
		setattr(cls, '__edmtype__', "".join(["EDM.", clsname]))
		type.__init__(cls, clsname, bases, _dict)


class _Type(object):
	__facets__ = ['Nullable', 'Name']
	__meta_node__ = ET.Element('Property')
	__metaclass__ = EDMElement

	def __init__(self, name, **facets):
		self.facets = {}
		self.facets['Name'] = str(name)
		self.meta_node.attrib['Name'] = str(name)
		self.meta_node.attrib['Type'] = self.__edmtype__
		for k,v in facets.items():
			if k in self.__facets__:
				self.facets[k] = v
				self.meta_node.attrib[k] = str(v)
			else:
				raise UnknownFacetError("Type {0} does not support facet {1}".format(self.__class__.__name__, k))

	@property
	def meta_node(self):
		raise NotImplementedError()

class _Stream(_Type):
	def __init__(self, name, **facets):
		self.__facets__.append('MaxLength')
		self.__facets__.append('FixedLength')
		super(_Stream, self).__init__(name, **facets)

class String(_Stream):
	def __init__(self, name, **facets):
		
		self.__facets__.append('Unicode')
		self.__facets__.append('DefaultValue')
		super(String, self).__init__(name, **facets)
	

	@property
	def meta_node(self):
		return self.__meta_node__


class Null(object):
	__meta_node__ = ET.Element('Property', Type="Null")

	def __init__(self, name):
		self.__meta_node__.attrib["Name"] = name

	@property
	def meta_node(self):
		return self.__meta_node__



class Binary(_Stream):
	def __init__(self, name, **facets):
		self.__repr_types__ = ['Hex', 'Base64']
		super(Binary, self).__init__(name, **facets)

	@property
	def meta_node(self):
		return self.__meta_node__


s = String("foo", Unicode = True, MaxLength=13)
node =  s.meta_node
debugger.set_trace()