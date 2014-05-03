from pdb import Pdb

debug = Pdb()

regex_base = {
    'ALPHA': '[A-Za-z]',
    'DIGIT': '[0-9]',
    'A-to-F': '[A-Fa-f]',
    'DQUOTE': '"',
    'SP': ' ',
    'HTAB': '\t',
    'VCHAR': '[\!-~]',
    'other-delims': '[!]|[\(]|[\)]|[\*]|[\+]|[,]|[;]'
}

regex_base['HEXDIG'] = "{}|{}".format(regex_base['DIGIT'], regex_base['A-to-F'])
regex_base['scheme'] = "{}({}|{}|\+|\-|\.)*".format(regex_base['ALPHA'], regex_base['ALPHA'], regex_base['DIGIT'])
regex_base['port'] = "{}*".format(regex_base['DIGIT'])
regex_base['h16'] = '[{}]{}'.format(regex_base['HEXDIG'], '{1,4}')
regex_base['dec-octet'] = '[1]{}{}|[2][0-4]{}|[2][5][0-5]|[1-9]{}|{}'.format(regex_base['DIGIT'], '{2}', regex_base['DIGIT'],regex_base['DIGIT'],regex_base['DIGIT'])
regex_base['unreserved'] = '{}|{}|[\-]|[\.]|[_]|[~]'.format(regex_base['ALPHA'], regex_base['DIGIT'])
regex_base['sub-delims'] = '[\$]|[\&]|[\']|[\=]|{}'.format(regex_base['other-delims'])
regex_base['IPv4address'] = '({})\.({})\.({})\.({})'.format(regex_base['dec-octet'],regex_base['dec-octet'],regex_base['dec-octet'],regex_base['dec-octet'])
regex_base['ls32'] = "{}:{}|{}".format(regex_base['h16'], regex_base['h16'], regex_base['IPv4address'])
regex_base['IPv6address'] = '{}{}:{}|::{}{}:{}|{}::{}{}:{}|{}:{}{}::{}{}:{}|{}:{}{}::{}{}:{}|{}:{}{}::{}:{}|{}:{}{}::{}|{}:{}{}::{}|{}:{}{}::'.format(regex_base['h16'], '{6}', regex_base['ls32'],
    regex_base['h16'], '{5}', regex_base['ls32'],
    regex_base['h16'], regex_base['h16'], '{4}', regex_base['ls32'],
    regex_base['h16'], '{0,1}', regex_base['h16'], regex_base['h16'], '{3}', regex_base['ls32'],
    regex_base['h16'], '{0,2}', regex_base['h16'], regex_base['h16'], '{2}', regex_base['ls32'],
    regex_base['h16'], '{0,3}', regex_base['h16'], regex_base['h16'], regex_base['ls32'],
    regex_base['h16'], '{0,4}', regex_base['h16'], regex_base['ls32'],
    regex_base['h16'], '{0,5}', regex_base['h16'], regex_base['h16'],
    regex_base['h16'], '{0,6}', regex_base['h16'])


debug.set_trace()