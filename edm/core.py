from edmtypes import *
from lxml import etree as ET
from pdb import Pdb

debug = Pdb()
ODATA_NAMESPACES = {
	'edmx': 'http://docs.oasis-open.org/odata/ns/edmx'
}
BOOLEAN_RANGE = [True, False]

class ComplexType(type):
	def __init__(cls, clsname, bases, _dict):
		if clsname != 'Base':
			valid_bases = filter(lambda x: x is not object and x.__name__ is not 'Base', bases)
			if len(valid_bases) == 1:
				doc_root = create_metadoc(cls, clsname, _dict, valid_bases[0])
			elif len(valid_bases) == 0:
				doc_root = create_metadoc(cls, clsname, _dict)
			else:
				raise TypeError("{} is not a valid OData entity, as it inherits from more than one base".format(clsname))
			setattr(cls, '__odata__', _dict)
			cls.__odata__['doc_root'] = doc_root
			for key in _dict:
				if hasattr(_dict[key], '__edmtype__'):
					setattr(cls, "".join(['_', key]), None)
					fget = _create_fget(key)
					fset = _create_fset(key)
					setattr(cls, key, property(fget, fset))
		type.__init__(cls, clsname, bases, _dict)

class EntityBase(ComplexType):
	def __init__(cls, clsname, bases, _dict):
		ComplexType.__init__(cls, clsname, bases, _dict)
		if '__stream__' in _dict:
			if _dict['__stream__'] in BOOLEAN_RANGE:
				cls.__odata__['doc_root'].attrib['HasStream'] = _dict['__stream__']
			else:
				raise ValueError('Invalid value for attribute "HasStream"')



def _create_fget(k):
	return lambda self: getattr(self, "".join(['_', k]))

def _create_fset(k):
	def fset(self, value):
		if self.__odata__[k].__regex__.match(value):
			setattr(self, "".join(['_', k]), value)
		else:
			raise ValueError('{0} is not a valid value for property of type {1}'.format(value, self.__odata__[k].__class__.__name__))
	return fset

def entity_base():
	return EntityBase("Base", (object, ), {})

def create_metadoc(cls, clsname, _dict, base = None):
	if 'key' not in _dict:
		raise TypeError("Invalid EntityType {}, EntityTypes must define a key".format(clsname))
	key_potent = filter(lambda x: hasattr(x,'facets') and x.facets['Name'] == _dict['key'] and x.key_valid, _dict.values())
	if len(key_potent) == 0:
		raise TypeError("Invalid EntityType {}, EntityTypes must define a key".format(clsname))
	entity_root = ET.Element('EntityType')
	if '__ename__' in _dict:
		entity_root.attrib['Name'] = _dict['__ename__']
		delattr(cls, '__ename__')
	else:
		entity_root.attrib['Name'] = clsname
	if base:
		entity_root.attrib['BaseType'] = base.__ename__ if '__ename__' in vars(base) else base.__name__
	if '__abstract__' in _dict:
		if dict['__abstract__'] in BOOLEAN_RANGE:
			entity_root.attrib['Abstract'] = _dict['__abstract__']
			if _dict['__abstract__']:
				setattr(cls, '__new__', abstract_new)
			delattr(cls, '__abstract__')
		else:
			raise ValueError('Invalid value for attribute "Abstract"')
	if '__opentype__' in _dict:
		if _dict['__opentype__'] in BOOLEAN_RANGE:
			entity_root.attrib['OpenType'] = _dict['__opentype__']
			delattr(cls, '__opentype__')
		else:
			raise ValueError('Invalid value for attribute "OpenType"')
	key_elem = ET.Element('Key')
	key_prop = ET.Element('PropertyRef')
	key_prop.attrib['Name'] = _dict['key']
	key_elem.append(key_prop)
	entity_root.append(key_elem)
	for k, v in _dict.items():
		if not k.startswith('_') and hasattr(v, 'meta_node'):
			entity_root.append(v.meta_node)
	return entity_root


def abstract_new(cls, *args, **kwargs):
	raise TypeError("Cannot create instance of an abstract class")

def gen_metadoc(entity_list):
	def append_meta_node(entity):
		if hasattr(entity, '__odata__') and 'doc_root' in entity.__odata__:
			service_node.append(entity.__odata__['doc_root'])
		else:
			raise TypeError("{} is not a valid OData entity".format(entity.__class__.__name__))
	root = ET.Element('{%s}EDMX' % ODATA_NAMESPACES['edmx'], nsmap=ODATA_NAMESPACES)
	root.attrib['Version'] = '4.0'
	base_ref_node = ET.Element('{%s}Reference' % ODATA_NAMESPACES['edmx'])
	base_ref_node.attrib['Uri'] = "http://docs.oasis-open.org/odata/odata/v4.0/cs01/vocabularies/Org.OData.Core.V1.xml"
	include_node = ET.Element('{%s}Inlcude' % ODATA_NAMESPACES['edmx'])
	include_node.attrib['Namespace'] = 'Org.OData.Core.V1'
	include_node.attrib['Alias'] = 'Core'
	base_ref_node.append(include_node)
	root.append(base_ref_node)
	measure_ref_node = ET.Element('{%s}Reference' % ODATA_NAMESPACES['edmx'])
	measure_ref_node.attrib['Uri'] = "http://docs.oasis-open.org/odata/odata/v4.0/cs01/vocabularies/Org.OData.Measures.V1.xml"
	measure_include_node = ET.Element('{%s}Include' % ODATA_NAMESPACES['edmx'])
	measure_include_node.attrib['Alias'] = 'UoM'
	measure_include_node.attrib['Namespace'] = 'Org.OData.Measures.V1'
	measure_ref_node.append(measure_include_node)
	root.append(measure_ref_node)
	service_node = ET.Element('{%s}DataServices' % ODATA_NAMESPACES['edmx'])
	[append_meta_node(entity) for entity in entity_list]
	root.append(service_node)
	return root


class Foo(entity_base()):
	key = 'foo'
	__ename__ = 'MyFoo'
	a = String("foo")

debug.set_trace()