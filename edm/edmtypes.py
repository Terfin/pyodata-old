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

regex_table = {
	'Int16': r'^((\+|%2b|\-)){0,1}[0-9]{1,5}$',
	'Int32': r'^((\+|%2b|\-)){0,1}[0-9]{1,10}$',
	'Int64': r'^((\+|%2b|\-)){0,1}[0-9]{1,19}$',
	'Binary': r'^(([-A-Z_a-z0-9]{4,4})*(([-A-Z_a-z0-9]{2,2}([AaEeIiMmQqUuYyCcGgKkOoSsWw]|0|4|8)(\=){0,1})|([-A-Z_a-z0-9][AaQqGgWw](\=\=){0,1})){0,1})$',
	'Boolean': r'^([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])$',
	'Byte': r'^[0-9]{1,3}$',
	'DateTimeOffset': r'^(((\-){0,1}(0[0-9]{3,3}|(1|2|3|4|5|6|7|8|9)[0-9]{3,}))\-(0(1|2|3|4|5|6|7|8|9)|1(0|1|2))\-(0(1|2|3|4|5|6|7|8|9)|(1|2)[0-9]|3(0|1))[Tt]((0|1)[0-9]|2(1|2|3))\:((0|1|2|3|4|5)[0-9])(\:((0|1|2|3|4|5)[0-9])(\.[0-9]{1,12}){0,1}){0,1}([Zz]|(\+|%2[Bb]|\-)((0|1)[0-9]|2(1|2|3))\:((0|1|2|3|4|5)[0-9])))$',
	'Decimal': r'^((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}$',
	'Double': r'^(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))$',
	'Single': r'^(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))$',
	'Guid': r'^[0-9A-Fa-f]{8,8}\-[0-9A-Fa-f]{4,4}\-[0-9A-Fa-f]{4,4}\-[0-9A-Fa-f]{4,4}\-[0-9A-Fa-f]{12,12}$',
	'SByte': r'^((\+|%2[Bb]|\-)){0,1}[0-9]{1,3}$',
	'Time': r'^((0|1)[0-9]|2(1|2|3))\:((0|1|2|3|4|5)[0-9])(\:((0|1|2|3|4|5)[0-9])(\.[0-9]{1,12}){0,1}){0,1}$',
	'Date': r'^((\-){0,1}(0[0-9]{3,3}|(1|2|3|4|5|6|7|8|9)[0-9]{3,}))\-(0(1|2|3|4|5|6|7|8|9)|1(0|1|2))\-(0(1|2|3|4|5|6|7|8|9)|(1|2)[0-9]|3(0|1))$',
	'GeographyPoint': r'^[Gg][Ee][Oo][Gg][Rr][Aa][Pp][Hh][Yy]('|%27)[Ss][Rr][Ii][Dd]\=[0-9]{1,5}(;|%3[Bb])[Pp][Oo][Ii][Nn][Tt](\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][FfIi][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][FfIi][Nn][Ff]))(\)|%29)('|%27)$',
	'GeographyLineString': r"^[Gg][Ee][Oo][Gg][Rr][Aa][Pp][Hh][Yy]('|%27)[Ss][Rr][Ii][Dd]\=[0-9]{1,5}(;|%3[Bb])[Ll][Ii][Nn][Ee][Ss][Tt][Rr][Ii][Nn][Gg](\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][FfIi][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][FfIi][Nn][Ff])))+(\)|%29)('|%27)$",
	'GeographyPolygon': r"^[Gg][Ee][Oo][Gg][Rr][Aa][Pp][Hh][Yy]('|%27)[Ss][Rr][Ii][Dd]\=[0-9]{1,5}(;|%3[Bb])[Pp][Oo][Ll][Yy][Gg][Oo][Nn](\(|%28)(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))*(\)|%29)((,|%2[Cc])(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))*(\)|%29))*(\)|%29)('|%27)$",
	'GeographyMultiPoint': r"^[Gg][Ee][Oo][Gg][Rr][Aa][Pp][Hh][Yy]('|%27)[Ss][Rr][Ii][Dd]\=[0-9]{1,5}(;|%3[Bb])[Mm][Uu][Ll][Tt][Ii][Pp][Oo][Ii][Nn][Tt]\(((\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))(\)|%29)((,|%2[Cc])(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))(\)|%29))*){0,1}(\)|%29)('|%27)$",
	'GeographyMultiLineString': r"^[Gg][Ee][Oo][Gg][Rr][Aa][Pp][Hh][Yy]('|%27)[Ss][Rr][Ii][Dd]\=[0-9]{1,5}(;|%3[Bb])[Mm][Uu][Ll][Tt][Ii][Ll][Ii][Nn][Ee][Ss][Tt][Rr][Ii][Nn][Gg]\(((\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))+(\)|%29)((,|%2[Cc])(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))+(\)|%29))*){0,1}(\)|%29)('|%27)$",
	'GeographyMultiPolygon': r"^[Gg][Ee][Oo][Gg][Rr][Aa][Pp][Hh][Yy]('|%27)[Ss][Rr][Ii][Dd]\=[0-9]{1,5}(;|%3[Bb])[Mm][Uu][Ll][Tt][Ii][Pp][Oo][Ll][Yy][Gg][Oo][Nn]\(((\(|%28)(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))*(\)|%29)((,|%2[Cc])(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))*(\)|%29))*(\)|%29)((,|%2[Cc])(\(|%28)(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))*(\)|%29)((,|%2[Cc])(\(|%28)(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff]))((,|%2[Cc])(((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])) (((\+|%2[Bb]|\-)){0,1}[0-9]+(\.[0-9]+){0,1}([Ee]((\+|%2[Bb]|\-)){0,1}[0-9]+){0,1}|([Nn][Aa][Nn]|\-[Ii][Nn][Ff]|\+[Ii][Nn][Ff])))*(\)|%29))*(\)|%29))*){0,1}(\)|%29)('|%27)$",
	
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
		super(Binary, self).__init__(name, **facets)


class Boolean(_PrimitiveType):
	def __init__(self, name, **facets):
		super(Boolean, self).__init__(name, **facets)


class Byte(_Number):
	def __init__(self, name, **facets):
		super(Byte, self).__init__(name, **facets)


class DateTimeOffset(_PrimitiveType):
	def __init__(self, name, **facets):
		super(DateTimeOffset, self).__init__(name, **facets)


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


class Date(_PrimitiveType):
	def __init__(self, name, **facets):
		super(Date, self).__init__(name, **facets)


class Geography(_PrimitiveType):
	def __init__(self, name, **facets):
		self.__facets__.append('SRID')
		super(Geography, self).__init__(name, **facets)


class GeographyPoint(Geography):
	def __init__(self, name, **facets):
		super(GeographyPoint, self).__init__(name, **facets)


class GeographyLineString(Geography):
	def __init__(self, name, **facets):
		super(GeographyLineString, self).__init__(name, **facets)


class GeographyPolygon(Geography):
	def __init__(self, name, **facets):
		super(GeographyPolygon, self).__init__(name, **facets)


class GeographyMultiPoint(Geography):
	def __init__(self, name, **facets):
		super(GeographyMultiPoint, self).__init__(name, **facets)


class GeographyMultiLineString(Geography):
	def __init__(self, name, **facets):
		super(GeographyMultiLineString, self).__init__(name, **facets)


class GeographyMultiPolygon(Geography):
	def __init__(self, name, **facets):
		super(GeographyMultiPolygon, self).__init__(name, **facets)


class GeographyCollection(Geography):
	def __init__(self, name, **facets):
		super(GeographyCollection, self).__init__(name, **facets)


class Geometry(_PrimitiveType):
	def __init__(self, name, **facets):
		self.__facets__.append('SRID')
		super(Geometry, self).__init__(name, **facets)


class GeometryPoint(Geometry):
	def __init__(self, name, **facets):
		super(GeometryPoint, self).__init__(name, **facets)


class GeometryLineString(Geometry):
	def __init__(self, name, **facets):
		super(GeometryLineString, self).__init__(name, **facets)


class GeometryPolygon(Geometry):
	def __init__(self, name, **facets):
		super(GeometryPolygon, self).__init__(name, **facets)


class GeometryMultiPoint(Geometry):
	def __init__(self, name, **facets):
		super(GeometryMultiPoint, self).__init__(name, **facets)


class GeometryMultiLineString(Geometry):
	def __init__(self, name, **facets):
		super(GeometryMultiLineString, self).__init__(name, **facets)


class GeometryMultiPolygon(Geometry):
	def __init__(self, name, **facets):
		super(GeometryMultiPolygon, self).__init__(name, **facets)


class GeometryCollection(Geometry):
	def __init__(self, name, **facets):
		super(GeometryCollection, self).__init__(name, **facets)


__all__ = ['String']
debugger.set_trace()