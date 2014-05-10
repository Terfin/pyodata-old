from edmtypes import *
from lxml import etree as ET
from pdb import Pdb

debug = Pdb()
ODATA_NAMESPACES = {
	'edmx': 'http://docs.oasis-open.org/odata/ns/edmx'
}


class EntityBase(type):
	def __init__(cls, clsname, bases, _dict):
		create_metadoc(cls, _dict)
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
	def fset(self, value):
		if self.__odata__[k].__regex__.match(value):
			setattr(self, "".join(['_', k]), value)
		else:
			raise ValueError('{0} is not a valid value for property of type {1}'.format(value, self.__odata__[k].__class__.__name__))
	return fset

def entity_base():
	return EntityBase("Base", (object, ), {})

def create_metadoc(cls, clsname, _dict, base = None):
	entity_root = ET.Element(clsname)
	if __ename__ in _dict:
		entity_root.attrib['Name'] = _dict['__ename__']
	if base:
		entity_root.attrib['BaseType'] = base.__ename__ if __ename__ in vars(base) else base.__name__
	if '__abstract__' in _dict:
		entity_root.attrib['Abstract'] = _dict['__abstract__']
		setattr(cls, '__new__', abstract_new)
	if '__opentype__' in _dict

def abstract_new(cls, *args, **kwargs):
	raise TypeError("Cannot create instance of an abstract class")

reserved = """
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
root.append(service_node)
"""

class Foo(entity_base()):
	a = String("foo")