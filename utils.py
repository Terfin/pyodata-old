from pdb import Pdb

debug = Pdb()

regex_base = {
    'ALPHA': '([A-Za-z])',
    'DIGIT': '([0-9])',
    'A-to-F': '([A-Fa-f])',
    'DQUOTE': '(")',
    'SP': '(\ )',
    'HTAB': '(\t)',
    'VCHAR': '([\!-~])',
    'other-delims': '([!]|[\(]|[\)]|[\*]|[\+]|[,]|[;])',
    'AT': '(@|%40)',
    'COLON': '(:|%3A)',
    'COMMA': '(,|%2C)',
    'EQ': '(\=)',
    'SIGN': '(\+|%2B|\-)',
    'SEMI': '(;|%3B)',
    'STAR': '(*|%2A)',
    'SQUOTE': '(\'|%27)',
    'OPEN': '(\(|%28)',
    'CLOSE': '(\)|%29)',
    'escape': '(\\|%5C)',
    'obs-text': '(%x80-FF)',
    'allowEntityReferencesPreference': "(odata.allow-entityreferences)",
    'continueOnErrorPreference': "(odata.continue-on-error)",
    'excludeOperator': '(\-)',
    'respondAsyncPreference': "(respond-async)",
    'trackChangesPreference': "(odata.track-changes)"
}

regex_base['HEXDIG'] = "({DIGIT}|{A-to-F})".format(**regex_base)
regex_base['scheme'] = "({ALPHA}({ALPHA}|{DIGIT}|\+|\-|\.)*)".format(**regex_base)
regex_base['port'] = "({}*)".format(regex_base['DIGIT'])
regex_base['h16'] = '([{}]{{1,4}})'.format(regex_base['HEXDIG'])
regex_base['dec-octet'] = '([1]{0}{{2}}|[2][0-4]{0}|[2][5][0-5]|[1-9]{0}|{0})'.format(regex_base['DIGIT'])
regex_base['unreserved'] = '({ALPHA}|{DIGIT}|[\-]|[\.]|[_]|[~])'.format(**regex_base)
regex_base['sub-delims'] = '([\$]|[\&]|[\']|[\=]|{})'.format(regex_base['other-delims'])
regex_base['IPv4address'] = '({0}\.{0}\.{0}\.{0})'.format(regex_base['dec-octet'])
regex_base['ls32'] = "{h16}:{h16}|{IPv4address}".format(**regex_base)
regex_base['IPv6address'] = '({h16}{{6}}:{ls32}|::{h16}{{5}}:{ls32}|{h16}::{h16}{{4}}:{{ls32}}|{h16}:{{0,1}}{h16}::{h16}{{3}}:{ls32}|{h16}:{{0,2}}{h16}::{h16}{{2}}:{ls32}|{h16}:{{0,3}}{h16}::{h16}:{ls32}|{h16}:{{0,4}}{h16}::{ls32}|{h16}:{{0,5}}{h16}::{h16}|{h16}:{{0,6}}{h16}::)'.format(**regex_base)
regex_base['pct-encoded'] = '(%({0}{0}))'.format(regex_base['HEXDIG'])
regex_base['pchar'] = '({unreserved}|{pct-encoded}|{sub-delims}|:|@)'.format(**regex_base)
regex_base['query'] = '({}|\/|\?)*'.format(regex_base['pchar'])
regex_base['fragment'] = '({}|\/|\?)*'.format(regex_base['pchar'])
regex_base['pct-encoded-no-SQUOTE'] = '([%][0-1]|[3-9]|{A-to-F}{HEXDIG}[%][2][0-6]|[8-9]|{A-to-F})'.format(**regex_base)
regex_base['qchar-no-AMP'] = '({unreserved}|{pct-encoded}|{other-delims}|:|@|\/|\?|\$|\'|\=)'.format(**regex_base)
regex_base['qchar-no-AMP-EQ'] = '({unreserved}|{pct-encoded}|{other-delims}|:|@|\/|\?|\$|\')'.format(**regex_base)
regex_base['qchar-no-AMP-EQ-AT-DOLLAR'] = '({unreserved}|{pct-encoded}|{other-delims}|:|\/|\?|\')'.format(**regex_base)
regex_base['pchar-no-SQUOTE'] = '({unreserved}|{pct-encoded-no-SQUOTE}|{other-delims}|\$|\&|\=|:|@)'.format(**regex_base)
regex_base['pct-encoded-unescaped'] = '([%][0-1]|[3-4]|[6-9]|{A-to-F}{HEXDIG}[%][2][0-1]|[3-9]|{A-to-F}|[%][5]{DIGIT}|[A-Ba-b]|[D-Fd-f])'.format(**regex_base)
regex_base['qchar-unescaped'] = '({unreserved}|{pct-encoded-unescaped}|{other-delims}|:|@|\/|\?|\$|\'|\=)'.format(**regex_base)
regex_base['OWS'] = '(({SP}|{HTAB}|%20|%09)*)'.format(**regex_base)
regex_base['RWS'] = '(({SP}|{HTAB}|%20|%09)+)'.format(**regex_base)
regex_base['BWS'] = regex_base['OWS']
regex_base['quotation-mark'] = '({}|%22)'.format(regex_base['DQUOTE'])
regex_base['qchar-no-AMP-DQUOTE'] = '({qchar-unescaped}|{escape}{escape}|{quotation-mark})'.format(**regex_base)
regex_base['IRI-in-query'] = '({})+'.format(regex_base['qchar-no-AMP'])
regex_base['segment'] = '({})*'.format(regex_base['pchar'])
regex_base['segment-nz'] = '({})+'.format(regex_base['pchar'])
regex_base['path-rootless'] = '({segment-nz}(\/{segment})*)'.format(**regex_base)
regex_base['path-absolute'] = '(\/({segment-nz}(\/{segment})*){{0,1}})'.format(**regex_base)
regex_base['path-abempty'] = '(\/{0})*'.format(regex_base['segment'])
regex_base['reg-name'] = '({unreserved}|{pct-encoded}|{sub-delims})*'.format(**regex_base)
regex_base['IPvFuture'] = '(v({HEXDIG})+\.({unreserved}|{sub-delims}|:)+)'.format(**regex_base)
regex_base['IP-literal'] = '(\[{IPv6address}|{IPvFuture}\])'.format(**regex_base)
regex_base['host'] = '({IP-literal}|{IPv4address}|{reg-name})'.format(**regex_base)
regex_base['userinfo'] = '(({unreserved}|{pct-encoded}|{sub-delims}|:)*)'.format(**regex_base)
regex_base['authority'] = '(({userinfo}@){{0,1}}{host}(:{port}){{0,1}})'.format(**regex_base)
regex_base['path-empty'] = ''
regex_base['hier-part'] = '(\/\/{authority}{path-abempty}|{path-absolute}|{path-rootless}|{path-empty})'.format(**regex_base)
regex_base['URI'] = '{scheme}:{hier-part}{query}{{0,1}}(\#{fragment}){{0,1}}'.format(**regex_base)
regex_base['content-id'] = '(CONTENT-ID{COLON}{OWS}{unreserved}+)'.format(**regex_base)
regex_base['IRI-in-header'] = '(({VCHAR}|{obs-text})+)'.format(**regex_base)
regex_base['odata-entityid'] = '(OData-EntityID{COLON}{OWS}{IRI-in-header})'.format(**regex_base)
regex_base['odata-isolation'] = '(OData-Isolation{COLON}{OWS}snapshot)'.format(**regex_base)
regex_base['odata-maxversion'] = '(OData-MaxVersion{COLON}{OWS}4.0)'.format(**regex_base)
regex_base['odata-version'] = '(OData-Version{COLON}{OWS}4.0)'.format(**regex_base)
regex_base['callbackPreference'] = '(odata.callback{OWS};{OWS}url{BWS}{EQ}{BWS}{DQUOTE}{URI}{DQUOTE})'.format(**regex_base)
regex_base['returnPreference'] = '(return{BWS}{EQ}{BWS}representation|minimal)'.format(**regex_base)
regex_base['waitPreference'] = '(wait{BWS}{EQ}{BWS}{DIGIT}+)'.format(**regex_base)
regex_base['identifierLeadingCharacter'] = '({}|_)'.format(regex_base['ALPHA'])
regex_base['identifierCharacter'] = '({ALPHA}|_|{DIGIT})'.format(**regex_base)
regex_base['odataIdentifier'] = '({identifierLeadingCharacter}{identifierCharacter}{{0,127}})'.format(**regex_base)
regex_base['namespacePart'] = regex_base['odataIdentifier']
regex_base['namespace'] = '({0}(\.{0})*)'.format(regex_base['namespacePart'])
regex_base['entitySetName'] = regex_base['odataIdentifier']
regex_base['singletonEntity'] = regex_base['odataIdentifier']
regex_base['complexTypeName'] = regex_base['odataIdentifier']
regex_base['typeDefinitionName'] = regex_base['odataIdentifier']
regex_base['enumerationTypeName'] = regex_base['odataIdentifier']
regex_base['enumerationMember'] = regex_base['odataIdentifier']
regex_base['termName'] = regex_base['odataIdentifier']
regex_base['annotationIdentifier'] = '({excludeOperator}{{0,1}}{STAR}|{namespace}\.{termName}|{STAR})'.format(**regex_base)
regex_base['annotationsList'] = '({annotationIdentifier}({COMMA}{annotationIdentifier})*)'.format(**regex_base)
regex_base['includeAnnotationsPreference'] = '(odata.include-annotations{BWS}{EQ}{BWS}{DQUOTE}{annotationsList}{DQUOTE})'.format(**regex_base)

debug.set_trace()