# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractproperty, abstractmethod
from pdb import Pdb
from lxml import etree as ET
from lxml import objectify

debugger = Pdb()

numeric_ranges = {
	'SByte': { '_minval': -2**7, '_maxval': 2**7 },
	'Int16': { '_maxval': 2**15, '_minval': -2**15 },
	'Int32': { '_maxval': 2**31, '_minval': -2**31 },
	'Int64': { '_maxval': 2**63, '_minval': -2**63 },
	'Double': { '_maxval': 1.7 * 10 ** 307, '_minval': -1.7 * 10 ** 307 }
}

formats_table = {
	'Time': ('%H:%M:%SZ', '%H:%M:%S-%H:%M', '%H:%M:%S+%H:%M')
	'DateTimeOffset': ('%Y:%m:%dT%H:%M:%SZ', '%Y:%m:%dT%H:%M:%S-%H:%M', '%Y:%m:%dT%H:%M:%S+%H:%M'),

}

class UnknownFacetError(AttributeError):
	pass

class _EDMElement(type):
	def __init__(cls, clsname, bases, _dict):
		setattr(cls, '__edmtype__', "".join(["EDM.", clsname]))
		if not hasattr(cls, '__regex__'):
			setattr(cls, '__format__', value)
		type.__init__(cls, clsname, bases, _dict)

class _EDMNumberElement(_EDMElement):
	def __init__(cls, clsname, bases, _dict):
		if numeric_ranges.has_key(clsname):
			setattr(cls, '_maxval', numeric_ranges[clsname]['_maxval'])
			setattr(cls, '_minval', numeric_ranges[clsname]['_minval'])
			setattr(cls, '__regex__', '[-][0-9]+')
		_EDMElement.__init__(cls, clsname, bases, _dict)

class _PrimitiveType(object):
	__facets__ = ['Nullable', 'Name', 'ConcurrencyMode']
	__meta_node__ = ET.Element('Property')
	__metaclass__ = _EDMElement

	def __init__(self, name, **facets):
		self.facets = {}
		self.facets['Name'] = str(name)
		self.meta_node.attrib['Name'] = str(name)
		self.meta_node.attrib['EDMType'] = self.__edmEDMType__
		for k,v in facets.items():
			if k in self.__facets__:
				self.facets[k] = v
				self.meta_node.attrib[k] = str(v)
			else:
				raise UnknownFacetError("EDMType {0} does not support facet {1}".format(self.__class__.__name__, k))

	@property
	def meta_node(self):
		return self.__meta_node__


class _Number(_PrimitiveType):
	__metaclass__ = _EDMWholeNumberElement
	def __init__(self, name, **facets):
		super(_Number, self).__init__(name, **facets)

class _Stream(_PrimitiveType):
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
	__meta_node__ = ET.Element('Property', EDMType="Null")

	def __init__(self, name):
		self.__meta_node__.attrib["Name"] = name


class Binary(_Stream):
	def __init__(self, name, **facets):
		self.__repr_PrimitiveTypes__ = ['Hex', 'Base64']
		self.__regex__ = '((A-F | a-f | 0-9)(A-F | a-f | 0-9))*'
		super(Binary, self).__init__(name, **facets)


class Boolean(_PrimitiveType):
	def __init__(self, name, **facets):
		self.__regex__ = '(true | false | 1 | 0'
		super(Boolean, self).__init__(name, **facets)


class Byte(_Number):
	def __init__(self, name, **facets):
		super(Byte, self).__init__(name, **facets)


class DateTime(_PrimitiveType):
	def __init__(self, name, **facets):
		self.__regex__ = 'yyyy “-” mm “-” dd “T” hh “:” mm [":" ss["." fffffff]]'
		super(DateTime, self).__init__(name, **facets)


class Decimal(_Number):
	def __init__(self, name, **facets):
		self.__facets__.append('Precision')
		self.__facets__.append('Scale')
		super(Decimal, self).__init__(name, **facets)


class Double(_Number):
	def __init__(self, name, **facets):
		super(Double, self).__init__(name, **facets)


class Single(_PrimitiveType):
	def __init__(self, name, **facets):
		super(Single, self).__init__(name, **facets)


class Guid(_PrimitiveType):
	def __init__(self, name, **facets):
		super(Guid, self).__init__(name, **facets)



class Int16(_Number):
	def __init__(self, name, **facets):
		super(Int16, self).__init__(name, **facets)


class Int32(_Number):
	def __init__(self, name, **facets):
		super(Int32, self).__init__(name, **facets)


class Int64(_Number):
	def __init__(self, name, **facets):
		super(Int64, self).__init__(name, **facets)


class SByte(_Number):
	def __init__(self, name, **facets):
		super(SByte, self).__init__(name, **facets)


class Time(_PrimitiveType):
	def __init__(self, name, **facets):
		self.__regex__ = 'hh “:” mm [":" ss["." fffffff]]'
		super(Time, self).__init__(name, **facets)


class DateTimeOffset(_PrimitiveType):
	def __init__(self, name, **facets):
		super(DateTimeOffset, self).__init__(name, **facets)


class Geography(_PrimitiveType):
	def __init__(self, name, **facets):
		self.__facets__.append('SRID')
		super(Geography, self).__init__(name, **facets)


class GeographyPoint(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeographyPoint, self).__init__(name, **facets)


class GeographyLineString(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeographyLineString, self).__init__(name, **facets)


class GeographyPolygon(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeographyPolygon, self).__init__(name, **facets)


class GeographyMultiPoint(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeographyMultiPoint, self).__init__(name, **facets)


class GeographyMultiLineString(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeographyMultiLineString, self).__init__(name, **facets)


class GeographyMultiPolygon(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeographyMultiPolygon, self).__init__(name, **facets)


class GeographyCollection(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeographyCollection, self).__init__(name, **facets)


class Geometry(_PrimitiveType):
	def __init__(self, name, **facets):
		self.__facets__.append('SRID')
		super(Geometry, self).__init__(name, **facets)


class GeometryPoint(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeometryPoint, self).__init__(name, **facets)


class GeometryLineString(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeometryLineString, self).__init__(name, **facets)


class GeometryPolygon(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeometryPolygon, self).__init__(name, **facets)


class GeometryMultiPoint(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeometryMultiPoint, self).__init__(name, **facets)


class GeometryMultiLineString(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeometryMultiLineString, self).__init__(name, **facets)


class GeometryMultiPolygon(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeometryMultiPolygon, self).__init__(name, **facets)


class GeometryCollection(_PrimitiveType):
	def __init__(self, name, **facets):
		super(GeometryCollection, self).__init__(name, **facets)


__all__ = ['String']
debugger.set_trace()