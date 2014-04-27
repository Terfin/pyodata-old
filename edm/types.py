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
	__facets__ = ['Nullable', 'Name', 'ConcurrencyMode']
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
		return self.__meta_node__

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


class Null(object):
	__meta_node__ = ET.Element('Property', Type="Null")

	def __init__(self, name):
		self.__meta_node__.attrib["Name"] = name


class Binary(_Stream):
	def __init__(self, name, **facets):
		self.__repr_types__ = ['Hex', 'Base64']
		super(Binary, self).__init__(name, **facets)


class Boolean(_Type):
	def __init__(self, name, **facets):
		super(Boolean, self).__init__(name, **facets)


class Byte(_Type):
	def __init__(self, name, **facets):
		super(Byte, self).__init__(name, **facets)


class DateTime(_Type):
	def __init__(self, name, **facets):
		super(DateTime, self).__init__(name, **facets)


class Decimal(_Type):
	def __init__(self, name, **facets):
		self.__facets__.append('Precision')
		self.__facets__.append('Scale')
		super(Decimal, self).__init__(name, **facets)


class Double(_Type):
	def __init__(self, name, **facets):
		super(Double, self).__init__(name, **facets)


class Single(_Type):
	def __init__(self, name, **facets):
		super(Single, self).__init__(name, **facets)


class Guid(_Type):
	def __init__(self, name, **facets):
		super(Guid, self).__init__(name, **facets)


class Int16(_Type):
	def __init__(self, name, **facets):
		super(Int16, self).__init__(name, **facets)


class Int32(_Type):
	def __init__(self, name, **facets):
		super(Int32, self).__init__(name, **facets)


class Int64(_Type):
	def __init__(self, name, **facets):
		super(Int64, self).__init__(name, **facets)


class SByte(_Type):
	def __init__(self, name, **facets):
		super(SByte, self).__init__(name, **facets)


class Time(_Type):
	def __init__(self, name, **facets):
		super(Time, self).__init__(name, **facets)


class DateTimeOffset(_Type):
	def __init__(self, name, **facets):
		super(DateTimeOffset, self).__init__(name, **facets)


class Geography(_Type):
	def __init__(self, name, **facets):
		self.__facets__.append('SRID')
		super(Geography, self).__init__(name, **facets)


class GeographyPoint(_Type):
	def __init__(self, name, **facets):
		super(GeographyPoint, self).__init__(name, **facets)


class GeographyLineString(_Type):
	def __init__(self, name, **facets):
		super(GeographyLineString, self).__init__(name, **facets)


class GeographyPolygon(_Type):
	def __init__(self, name, **facets):
		super(GeographyPolygon, self).__init__(name, **facets)


class GeographyMultiPoint(_Type):
	def __init__(self, name, **facets):
		super(GeographyMultiPoint, self).__init__(name, **facets)


class GeographyMultiLineString(_Type):
	def __init__(self, name, **facets):
		super(GeographyMultiLineString, self).__init__(name, **facets)


class GeographyMultiPolygon(_Type):
	def __init__(self, name, **facets):
		super(GeographyMultiPolygon, self).__init__(name, **facets)


class GeographyCollection(_Type):
	def __init__(self, name, **facets):
		super(GeographyCollection, self).__init__(name, **facets)


class Geometry(_Type):
	def __init__(self, name, **facets):
		self.__facets__.append('SRID')
		super(Geometry, self).__init__(name, **facets)


class GeometryPoint(_Type):
	def __init__(self, name, **facets):
		super(GeometryPoint, self).__init__(name, **facets)


class GeometryLineString(_Type):
	def __init__(self, name, **facets):
		super(GeometryLineString, self).__init__(name, **facets)


class GeometryPolygon(_Type):
	def __init__(self, name, **facets):
		super(GeometryPolygon, self).__init__(name, **facets)


class GeometryMultiPoint(_Type):
	def __init__(self, name, **facets):
		super(GeometryMultiPoint, self).__init__(name, **facets)


class GeometryMultiLineString(_Type):
	def __init__(self, name, **facets):
		super(GeometryMultiLineString, self).__init__(name, **facets)


class GeometryMultiPolygon(_Type):
	def __init__(self, name, **facets):
		super(GeometryMultiPolygon, self).__init__(name, **facets)


class GeometryCollection(_Type):
	def __init__(self, name, **facets):
		super(GeometryCollection, self).__init__(name, **facets)

s = String("foo", Unicode = True, MaxLength=13)
node =  s.meta_node
debugger.set_trace()