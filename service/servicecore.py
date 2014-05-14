from lxml import etree as ET
from base64 import b64encode
from hashlib import md5

ODATA_NAMESPACES = {
	'atom': 'http://www.w3.org/2005/Atom',
	'metadata': 'http://docs.oasis-open.org/odata/ns/metadata',
}
root = ET.Element('service', nsmap=ODATA_NAMESPACES)
root.attrib['xmlns'] = 	'http://www.w3.org/2007/app'
root.attrib['{%s}context' % ODATA_NAMESPACES['metadata']] = '$metadata'
workspace = ET.Element('workspace')
root.append(workspace)

# class Hashable(type):
# 	def __init__(cls, clsname, bases, _dict):
# 		hasher = md5()
# 		hasher.


class Service(object):
	etag = False
	def __init__(self, **kwargs):
		if 'etag' in kwargs:
			self.etag = kwargs['etag']
			# Should include a hashing of the final service document.

	def __str__(self):
		service_doc = ET.tostring(root)
		if self.etag:
			b64_doc = b32encode(service_doc)
			root.attrib['{%s}metadata-etag' % ODATA_NAMESPACES['metadata']] = "/W'{}'".format(b64_doc)
		return ET.tostring(root)
		

print Service(etag = True)
