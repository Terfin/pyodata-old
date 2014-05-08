import re
import utils
from pdb import Pdb

debug = Pdb()
print utils.regex_base['primitiveLiteral']
a = re.compile("^({})$".format(utils.regex_base['primitiveLiteral']))
b= a.match('Collection(Point(+133%x20-133))')
debug.set_trace()