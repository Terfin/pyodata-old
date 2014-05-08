from pdb import Pdb
from pyparsing import *

debug = Pdb()

regex_base = {
    'ALPHA': '[A-Za-z]',
    'DIGIT': '[0-9]',
    'A-to-F': '[A-Fa-f]',
    'DQUOTE': '"',
    'SP': '%x20',
    'HTAB': '%x09',
    'VCHAR': '(?:\\\\|!|-|~)',
    'other-delims': '(?:!|\(|\)|\*|\+|,|;)',
    'AT': '(?:@|%40)',
    'COLON': '(?::|%3A)',
    'COMMA': '(?:,|%2C)',
    'EQ': '\=',
    'SIGN': '(?:\+|%2B|\-)',
    'SEMI': '(?:;|%3B)',
    'STAR': '(?:\\*|%2A)',
    'SQUOTE': '(?:\'|%27)',
    'OPEN': '(?:\\(|%28)',
    'CLOSE': '(?:\\)|%29)',
    'escape': '(?:\\|%5C)',
    'obs-text': '(?:[%x80-FF])',
    'allowEntityReferencesPreference': "odata.allow-entityreferences",
    'continueOnErrorPreference': "odata.continue-on-error",
    'excludeOperator': '\-',
    'respondAsyncPreference': "respond-async",
    'trackChangesPreference': "odata.track-changes",
    'oneToNine': '[1-9]',
    'nullValue': 'null',
    'booleanValue': '(?:true|false)',
    'nanInfinity': '(?:NaN|\\-INF|\\+INF)',
    'geographyPrefix': 'geography',
    'geometryPrefix': 'geometry',
    'concreteSpatialTypeName': '(?:Collection|LineString|MultiLineString|MultiPoint|MultiPolygon|Point|Polygon)',
    'abstractSpatialTypeName': '(?:Geography|Geometry)',
}

regex_base['HEXDIG'] = "(?:{DIGIT}|{A-to-F})".format(**regex_base)
regex_base['scheme'] = "(?:{ALPHA}(?:{ALPHA}|{DIGIT}|\+|\-|\.)*)".format(**regex_base)
regex_base['port'] = "(?:{}*)".format(regex_base['DIGIT'])
regex_base['h16'] = '(?:{}{{1,4}})'.format(regex_base['HEXDIG'])
regex_base['dec-octet'] = '(?:(?:1{0}){{2}}|(?:2[0-4]{0})|(?:25[0-5])|(?:[1-9]{0})|{0})'.format(regex_base['DIGIT'])
regex_base['unreserved'] = '(?:{ALPHA}|{DIGIT}|[\-]|(?:\.|_|~))'.format(**regex_base)
regex_base['sub-delims'] = '(?:\$|\&|\'|\=|{})'.format(regex_base['other-delims'])
regex_base['IPv4address'] = '(?:{0}\.{0}\.{0}\.{0})'.format(regex_base['dec-octet'])
regex_base['ls32'] = "(?:(?:{h16}:{h16})|{IPv4address})".format(**regex_base)
regex_base['IPv6address'] = '(?:(?:{h16}:){{6}}{ls32})|(?:::(?:{h16}:){{5}}{ls32})|(?:{h16}{{0,1}}::(?:{h16}:){{4}}{ls32})|(?:(?:(?:{h16}:){{0,1}}{h16}){{0,1}}::(?:{h16}:){{3}}{ls32})|(?:(?:(?:{h16}:){{0,2}}{h16}){{0,1}}::(?:{h16}:){{2}}{ls32})|(?:(?:(?:{h16}:){{0,3}}{h16}){{0,1}}::{h16}:{ls32})|(?:(?:(?:{h16}:){{0,4}}{h16}){{0,1}}::{ls32})|(?:(?:(?:{h16}:){{0,5}}{h16}){{0,1}}::{h16})|(?:(?:(?:{h16}:){{0,6}}{h16}){{0,1}}::)'.format(**regex_base)
regex_base['pct-encoded'] = '%(?:{0}{0})'.format(regex_base['HEXDIG'])
regex_base['pchar'] = '(?:{unreserved}|{pct-encoded}|{sub-delims}|:|@)'.format(**regex_base)
regex_base['query'] = '(?:(?:{}|\/|\?)*)'.format(regex_base['pchar'])
regex_base['fragment'] = '(?:(?:{}|\/|\?)*)'.format(regex_base['pchar'])
regex_base['pct-encoded-no-SQUOTE'] = '(?:[%][0-1]|[3-9]|{A-to-F}{HEXDIG}[%][2][0-6]|[8-9]|{A-to-F})'.format(**regex_base)
regex_base['qchar-no-AMP'] = '(?:{unreserved}|{pct-encoded}|{other-delims}|:|@|\/|\?|\$|\'|\=)'.format(**regex_base)
regex_base['qchar-no-AMP-EQ'] = '(?:{unreserved}|{pct-encoded}|{other-delims}|:|@|\/|\?|\$|\')'.format(**regex_base)
regex_base['qchar-no-AMP-EQ-AT-DOLLAR'] = '(?:{unreserved}|{pct-encoded}|{other-delims}|:|\/|\?|\')'.format(**regex_base)
regex_base['pchar-no-SQUOTE'] = '(?:{unreserved}|{pct-encoded-no-SQUOTE}|{other-delims}|\$|\&|\=|:|@)'.format(**regex_base)
regex_base['pct-encoded-unescaped'] = '(?:%[0-1]|[3-4]|[6-9]|{A-to-F}{HEXDIG}%2[0-1]|[3-9]|{A-to-F}|[%][5]{DIGIT}|[A-Ba-b]|[D-Fd-f])'.format(**regex_base)
regex_base['qchar-unescaped'] = '(?:{unreserved}|{pct-encoded-unescaped}|{other-delims}|:|@|\/|\?|\$|\'|\=)'.format(**regex_base)
regex_base['OWS'] = '(?:(?:{SP}|{HTAB}|%20|%09)*)'.format(**regex_base)
regex_base['RWS'] = '(?:(?:{SP}|{HTAB}|%20|%09)+)'.format(**regex_base)
regex_base['BWS'] = regex_base['OWS']
regex_base['quotation-mark'] = '(?:{}|%22)'.format(regex_base['DQUOTE'])
regex_base['qchar-no-AMP-DQUOTE'] = '(?:{qchar-unescaped}|{escape}{escape}|{quotation-mark})'.format(**regex_base)
regex_base['IRI-in-query'] = '(?:{}+)'.format(regex_base['qchar-no-AMP'])
regex_base['segment'] = '(?:{}*)'.format(regex_base['pchar'])
regex_base['segment-nz'] = '(?:{}+)'.format(regex_base['pchar'])
regex_base['path-rootless'] = '(?:{segment-nz}(?:\/{segment})*)'.format(**regex_base)
regex_base['path-absolute'] = '(?:\/(?:{segment-nz}(?:\/{segment})*){{0,1}})'.format(**regex_base)
regex_base['path-abempty'] = '(?:(?:\/{0})*)'.format(regex_base['segment'])
regex_base['reg-name'] = '(?:(?:{unreserved}|{pct-encoded}|{sub-delims})*)'.format(**regex_base)
regex_base['IPvFuture'] = '(?:v(?:{HEXDIG})+\.(?:{unreserved}|{sub-delims}|:)+)'.format(**regex_base)
regex_base['IP-literal'] = '(?:\[(?:{IPv6address}|{IPvFuture})\])'.format(**regex_base)
regex_base['host'] = '(?:{IP-literal}|{IPv4address}|{reg-name})'.format(**regex_base)
regex_base['userinfo'] = '(?:{unreserved}|{pct-encoded}|{sub-delims}|:)*'.format(**regex_base)
regex_base['authority'] = '(?:(?:{userinfo}@){{0,1}}{host}(?::{port}){{0,1}})'.format(**regex_base)
regex_base['path-empty'] = ''
regex_base['hier-part'] = '(?:\/\/{authority}(?:{path-abempty}|{path-absolute}|{path-rootless}|{path-empty}))'.format(**regex_base)
regex_base['URI'] = '(?:{scheme}:{hier-part}{query}{{0,1}}(?:\#{fragment}){{0,1}})'.format(**regex_base)
regex_base['content-id'] = '(?:CONTENT-ID{COLON}{OWS}{unreserved}+)'.format(**regex_base)
regex_base['IRI-in-header'] = '(?:(?:{VCHAR}|{obs-text})+)'.format(**regex_base)
regex_base['odata-entityid'] = '(?:OData-EntityID{COLON}{OWS}{IRI-in-header})'.format(**regex_base)
regex_base['odata-isolation'] = '(?:OData-Isolation{COLON}{OWS}snapshot)'.format(**regex_base)
regex_base['odata-maxversion'] = '(?:OData-MaxVersion{COLON}{OWS}4.0)'.format(**regex_base)
regex_base['odata-version'] = '(?:OData-Version{COLON}{OWS}4.0)'.format(**regex_base)
regex_base['callbackPreference'] = '(?:odata.callback{OWS};{OWS}url{BWS}{EQ}{BWS}{DQUOTE}{URI}{DQUOTE})'.format(**regex_base)
regex_base['returnPreference'] = '(?:return{BWS}{EQ}{BWS}(?:representation|minimal))'.format(**regex_base)
regex_base['waitPreference'] = '(?:wait{BWS}{EQ}{BWS}{DIGIT}+)'.format(**regex_base)
regex_base['identifierLeadingCharacter'] = '(?:{}|_)'.format(regex_base['ALPHA'])
regex_base['identifierCharacter'] = '(?:{ALPHA}|_|{DIGIT})'.format(**regex_base)
regex_base['odataIdentifier'] = '(?:{identifierLeadingCharacter}{identifierCharacter}{{0,127}})'.format(**regex_base)
regex_base['namespacePart'] = regex_base['odataIdentifier']
regex_base['namespace'] = '(?:{0}(?:\.{0})*)'.format(regex_base['namespacePart'])
regex_base['entitySetName'] = regex_base['odataIdentifier']
regex_base['singletonEntity'] = regex_base['odataIdentifier']
regex_base['complexTypeName'] = regex_base['odataIdentifier']
regex_base['typeDefinitionName'] = regex_base['odataIdentifier']
regex_base['enumerationTypeName'] = regex_base['odataIdentifier']
regex_base['enumerationMember'] = regex_base['odataIdentifier']
regex_base['termName'] = regex_base['odataIdentifier']
regex_base['annotationIdentifier'] = '(?:{excludeOperator}{{0,1}}(?:{STAR}|{namespace})\.(?:{termName}|{STAR}))'.format(**regex_base)
regex_base['annotationsList'] = '(?:{annotationIdentifier}(?:{COMMA}{annotationIdentifier})*)'.format(**regex_base)
regex_base['includeAnnotationsPreference'] = '(?:odata.include-annotations{BWS}{EQ}{BWS}{DQUOTE}{annotationsList}{DQUOTE})'.format(**regex_base)
regex_base['maxpagesizePreference'] = '(?:odata.maxpagesize{BWS}{EQ}{BWS}{oneToNine}{DIGIT}*)'.format(**regex_base)
regex_base['preference'] = '(?:{allowEntityReferencesPreference}|{callbackPreference}|{continueOnErrorPreference}|{includeAnnotationsPreference}|{maxpagesizePreference}|{respondAsyncPreference}|{returnPreference}|{trackChangesPreference}|{waitPreference})'.format(**regex_base)
regex_base['prefer'] = '(?:Prefer{COLON}{OWS}{preference}(?:{COMMA}{preference})*)'.format(**regex_base)
regex_base['header'] = '(?:{content-id}|{odata-entityid}|{odata-isolation}|{odata-maxversion}|{odata-version}|{prefer})'.format(**regex_base)
regex_base['sridLiteral'] = '(?:SRID{EQ}{DIGIT}{{1,5}}{SEMI})'.format(**regex_base)
regex_base['zeroToFiftyNine'] = '(?:[0-5]{})'.format(regex_base['DIGIT'])
regex_base['year'] = '(?:\-{{0,1}}(?:(?:0{DIGIT}{{3}})|(?:{oneToNine}{DIGIT}{{3,}})))'.format(**regex_base)
regex_base['month'] = '(?:(?:0{})|(?:1[0-2]))'.format(regex_base['oneToNine'])
regex_base['day'] = '((?:0{oneToNine})|(?:[1-2]{DIGIT})|(?:3[0-1]))'.format(**regex_base)
regex_base['hour'] = '(?:[0-1]{})|(?:2[1-3])'.format(regex_base['DIGIT'])
regex_base['minute'] = regex_base['zeroToFiftyNine']
regex_base['second'] = regex_base['zeroToFiftyNine']
regex_base['fractionalSeconds'] = '(?:{}{{1,12}})'.format('DIGIT')
regex_base['timeOfDayValue'] = '(?:{hour}:{minute}:{second}:(?:\.{fractionalSeconds}){{0,1}})'.format(**regex_base)
regex_base['durationValue'] = '(?:{SIGN}{{0,1}}P(?:{DIGIT}+D){{0,1}}(?:T(?:{DIGIT}+H){{0,1}}(?:{DIGIT}+M){{0,1}}(?:{DIGIT}+(?:\.{DIGIT}+){{0,1}}S){{0,1}}){{0,1}})'.format(**regex_base)
regex_base['base64char'] = '(?:{ALPHA}|{DIGIT}|-|_)'.format(**regex_base)
regex_base['base64b8'] = '(?:{base64char}(A|Q|g|w)(==){{0,1}})'.format(**regex_base)
regex_base['base64b16'] = '(?:{}{{2}}(?:A|E|I|M|Q|U|Y|c|g|k|o|s|w|0|4|8)(==){{0,1}})'.format(regex_base['base64char'])
regex_base['binaryValue'] = '(?:(?:(?:{base64char}{{4}})*)(?:{base64b16}|{base64b8}))'.format(**regex_base)
regex_base['binary'] = '(?:binary{SQUOTE}{binaryValue}{SQUOTE})'.format(**regex_base)
regex_base['decimalValue'] = '(?:{SIGN}{{0,1}}{DIGIT}+(?:\.{DIGIT}+){{0,1}})'.format(**regex_base)
regex_base['doubleValue'] = '(?:(?:{decimalValue}(?:e{SIGN}{{0,1}}{DIGIT}+){{0,1}}|{nanInfinity}){{0,1}})'.format(**regex_base)
regex_base['singleValue'] = regex_base['doubleValue']
regex_base['guidValue'] = '(?:{0}{{8}}\-{0}{{4}}\-{0}{{4}}\-{0}{{4}}\-{0}{{12}})'.format(regex_base['HEXDIG'])
regex_base['byteValue'] = '(?:{}{{1,3}})'.format(regex_base['DIGIT'])
regex_base['sbyteValue'] = '(?:{SIGN}{{0,1}}{DIGIT}{{1,3}})'.format(**regex_base)
regex_base['int16Value'] = '(?:{SIGN}{{0,1}}{DIGIT}{{1,5}})'.format(**regex_base)
regex_base['int32Value'] = '(?:{SIGN}{{0,1}}{DIGIT}{{1,10}})'.format(**regex_base)
regex_base['int64Value'] = '(?:{SIGN}{{0,1}}{DIGIT}{{1,19}})'.format(**regex_base)
regex_base['SQUOTE-in-string'] = '{0}{0}'.format(regex_base['SQUOTE'])
regex_base['string'] = '(?:{SQUOTE}(?:{SQUOTE-in-string}|{pchar-no-SQUOTE})*{SQUOTE})'.format(**regex_base)
regex_base['dateValue'] = '(?:{year}\-{month}\-{day})'.format(**regex_base)
regex_base['dateTimeOffsetValue'] = '(?:{year}\-{month}\-{day}T{hour}:{minute}(?:{second}(?:\.{fractionalSeconds}){{0,1}}){{0,1}})'.format(**regex_base)
regex_base['enumMemberValue'] = regex_base['int64Value']
regex_base['singleEnumValue'] = '(?:{enumerationMember}|{enumMemberValue})'.format(**regex_base)
regex_base['enumValue'] = '(?:{singleEnumValue}(?:{COMMA}{singleEnumValue})*)'.format(**regex_base)
regex_base['qualifiedEnumTypeName'] = '(?:{namespace}\.{enumerationTypeName})'.format(**regex_base)
regex_base['enum'] = '(?:{qualifiedEnumTypeName}{SQUOTE}{enumValue}{SQUOTE})'.format(**regex_base)
regex_base['positionLiteral'] = '(?:{doubleValue}{SP}{doubleValue})'.format(**regex_base)
regex_base['lineStringData'] = '(?:{OPEN}{positionLiteral}(?:{COMMA}{positionLiteral})*{CLOSE})'.format(**regex_base)
regex_base['lineStringLiteral'] = '(?:LineString{})'.format(regex_base['lineStringData'])
regex_base['fullLineStringLiteral'] = '(?:{sridLiteral}{lineStringLiteral})'.format(**regex_base)
regex_base['geographyLineString'] = '(?:{geographyPrefix}{SQUOTE}{fullLineStringLiteral}{SQUOTE})'.format(**regex_base)
regex_base['multiLineStringLiteral'] = '(?:MultiLineString\((?:{lineStringData}(?:{COMMA}{lineStringData})*){{0,1}}{CLOSE})'.format(**regex_base)
regex_base['fullMultiLineStringLiteral'] = '(?:{sridLiteral}{multiLineStringLiteral})'.format(**regex_base)
regex_base['geographyMultiLineString'] = '(?:{geographyPrefix}{SQUOTE}{fullMultiLineStringLiteral}{SQUOTE})'.format(**regex_base)
regex_base['pointData'] = '(?:{OPEN}{positionLiteral}{CLOSE})'.format(**regex_base)
regex_base['pointLiteral'] = '(?:Point{})'.format(regex_base['pointData'])
regex_base['fullPointLiteral'] = '(?:{sridLiteral}{pointLiteral})'.format(**regex_base)
regex_base['geographyPoint'] = '(?:{geographyPrefix}{SQUOTE}{fullPointLiteral}{SQUOTE})'.format(**regex_base)
regex_base['multiPointLiteral'] = '(?:MultiPoint\((?:{pointData}(?:{COMMA}{pointData})*){{0,1}}{CLOSE})'.format(**regex_base)
regex_base['fullMultiPointLiteral'] = '(?:{sridLiteral}{multiPointLiteral})'.format(**regex_base)
regex_base['geographyMultiPoint'] = '(?:{geographyPrefix}{SQUOTE}{fullMultiPointLiteral}{SQUOTE})'.format(**regex_base)
regex_base['ringLiteral'] = '(?:{OPEN}{positionLiteral}(?:{COMMA}{positionLiteral})*{CLOSE})'.format(**regex_base)
regex_base['polygonData'] = '(?:{OPEN}{ringLiteral}(?:{COMMA}{ringLiteral})*{CLOSE})'.format(**regex_base)
regex_base['polygonLiteral'] = '(?:Polygon{})'.format(regex_base['polygonData'])
regex_base['fullPolygonLiteral'] = '(?:{sridLiteral}{polygonLiteral})'.format(**regex_base)
regex_base['geographyPolygon'] = '(?:{geographyPrefix}{SQUOTE}{fullPolygonLiteral}{SQUOTE})'.format(**regex_base)
regex_base['multiPolygonLiteral'] = '(?:MultiPolygon\((?:{polygonData}(?:{COMMA}{polygonData})*){{0,1}}{CLOSE})'.format(**regex_base)
regex_base['fullMultiPolygonLiteral'] = '(?:{sridLiteral}{multiPolygonLiteral})'.format(**regex_base)
regex_base['geographyMultiPolygon'] = '(?:{geographyPrefix}{SQUOTE}{fullMultiPolygonLiteral}{SQUOTE})'.format(**regex_base)
regex_base['geoLiteral'] = '(?:{lineStringLiteral}|{multiPointLiteral}|{multiLineStringLiteral}|{multiPolygonLiteral}|{pointLiteral}|{polygonLiteral})'.format(**regex_base)
regex_base['collectionLiteral'] = '(?:Collection\({geoLiteral}(?:{COMMA}{geoLiteral})*{CLOSE})'.format(**regex_base)
regex_base['fullGeoLiteral'] = '(?:{collectionLiteral}|{geoLiteral})'.format(**regex_base)
regex_base['collectionOfCollectionLiteral'] = '(?:Collection\({fullGeoLiteral}(?:{COMMA}{fullGeoLiteral})*{CLOSE})'.format(**regex_base)
regex_base['fullCollectionLiteral'] = '(?:{sridLiteral}(?:{collectionOfCollectionLiteral}|{geoLiteral}))'.format(**regex_base)
regex_base['geographyCollection'] = '(?:{geographyPrefix}{SQUOTE}{fullCollectionLiteral}{SQUOTE})'.format(**regex_base)
regex_base['primitiveValue'] = '(?:{booleanValue}|{guidValue}|{durationValue}|{dateValue}|{dateTimeOffsetValue}|{timeOfDayValue}|{enumValue}|{fullCollectionLiteral}|{fullLineStringLiteral}|{fullMultiPointLiteral}|{fullMultiLineStringLiteral}|{fullPolygonLiteral}|{fullPointLiteral}|{fullPolygonLiteral}|{decimalValue}|{doubleValue}|{singleValue}|{sbyteValue}|{byteValue}|{int16Value}|{int32Value}|{int64Value}|{binaryValue})'.format(**regex_base)
regex_base['geometryCollection']= '(?:{geometryPrefix}{SQUOTE}{fullCollectionLiteral}{SQUOTE})'.format(**regex_base)
regex_base['geometryLineString']= '(?:{geometryPrefix}{SQUOTE}{fullLineStringLiteral}{SQUOTE})'.format(**regex_base)
regex_base['geometryMultiLineString']= '(?:{geometryPrefix}{SQUOTE}{fullMultiLineStringLiteral}{SQUOTE})'.format(**regex_base)
regex_base['geometryMultiPoint']= '(?:{geometryPrefix}{SQUOTE}{fullMultiPointLiteral}{SQUOTE})'.format(**regex_base)
regex_base['geometryMultiPolygon']= '(?:{geometryPrefix}{SQUOTE}{fullMultiPolygonLiteral}{SQUOTE})'.format(**regex_base)
regex_base['geometryPoint']= '(?:{geometryPrefix}{SQUOTE}{fullPointLiteral}{SQUOTE})'.format(**regex_base)
regex_base['geometryPolygon']= '(?:{geometryPrefix}{SQUOTE}{fullPolygonLiteral}{SQUOTE})'.format(**regex_base)
regex_base['duration'] = '(?:duration{SQUOTE}{durationValue}{SQUOTE})'.format(**regex_base)
regex_base['primitiveLiteral'] = '(?:{nullValue}|{booleanValue}|{guidValue}|{dateValue}|{dateTimeOffsetValue}|{timeOfDayValue}|{decimalValue}|{doubleValue}|{singleValue}|{sbyteValue}|{byteValue}|{int16Value}|{int32Value}|{int64Value}|{string}|{duration}|{binary}|{enum}|{geographyCollection}|{geographyLineString}|{geographyMultiLineString}|{geographyMultiPoint}|{geographyMultiPolygon}|{geographyPoint}|{geographyPolygon}|{geometryCollection}|{geometryLineString}|{geometryMultiLineString}|{geometryMultiPoint}|{geometryMultiPolygon}|{geometryPoint}|{geometryPolygon})'.format(**regex_base)
regex_base['entityFunctionImport'] = regex_base['odataIdentifier']
regex_base['entityColFunctionImport'] = regex_base['odataIdentifier']
regex_base['complexFunctionImport'] = regex_base['odataIdentifier']
regex_base['complexColFunctionImport'] = regex_base['odataIdentifier']
regex_base['primitiveFunctionImport'] = regex_base['odataIdentifier']
regex_base['primitiveColFunctionImport'] = regex_base['odataIdentifier']
regex_base['entityFunction'] = regex_base['odataIdentifier']
regex_base['entityColFunction'] = regex_base['odataIdentifier']
regex_base['complexFunction'] = regex_base['odataIdentifier']
regex_base['complexColFunction'] = regex_base['odataIdentifier']
regex_base['primitiveFunction'] = regex_base['odataIdentifier']
regex_base['primitiveColFunction'] = regex_base['odataIdentifier']
regex_base['function'] = regex_base['odataIdentifier']
regex_base['action'] = regex_base['odataIdentifier']
regex_base['actionImport'] = regex_base['odataIdentifier']
regex_base['entityColNavigationProperty'] = regex_base['odataIdentifier']
regex_base['entityNavigationProperty'] = regex_base['odataIdentifier']
regex_base['navigationProperty'] = regex_base['odataIdentifier']
regex_base['streamProperty'] = regex_base['odataIdentifier']
regex_base['complexColProperty'] = regex_base['odataIdentifier']
regex_base['complexProperty'] = regex_base['odataIdentifier']
regex_base['primitiveColProperty'] = regex_base['odataIdentifier']
regex_base['primitiveNonKeyProperty'] = regex_base['odataIdentifier']
regex_base['primitiveKeyProperty'] = regex_base['odataIdentifier']
regex_base['primitiveProperty'] = regex_base['odataIdentifier']
regex_base['primitiveTypeName'] = '(?:Edm\.(?:Binary|Boolean|Byte|Date|DateTimeOffset|Decimal|Double|Duration|Guid|Int16|Int32|Int64|SByte|Single|Stream|String|TimeOfDay|(?:{abstractSpatialTypeName}{concreteSpatialTypeName}{{0,1}})))'.format(**regex_base)
regex_base['entityTypeName'] = regex_base['odataIdentifier']
regex_base['qualifiedEntityTypeName'] = '(?:{namespace}\.{entityTypeName})'.format(**regex_base)
regex_base['qualifiedComplexTypeName'] = '(?:{namespace}\.{complexTypeName})'.format(**regex_base)
regex_base['qualifiedTypeDefinitionName'] = '(?:{namespace}\.{typeDefinitionName})'.format(**regex_base)
regex_base['singleQualifiedTypeName'] = '(?:{odataIdentifier}|{primitiveTypeName})'.format(**regex_base)
regex_base['qualifiedTypeName'] = '(?:{singleQualifiedTypeName}|(?:Collection{OPEN}{singleQualifiedTypeName}{CLOSE}))'.format(**regex_base)
regex_base['exp'] = '(?:e(?:\-|\+){{0,1}}{}+)'.format(regex_base['DIGIT'])
regex_base['frac'] = '(?:\.{}+)'.format(regex_base['DIGIT'])
regex_base['int'] = '(?:0|(?:{oneToNine}{DIGIT}*))'.format(**regex_base)
regex_base['numberInJSON'] = '(?:\-{{0,1}}{int}{frac}{{0,1}}{exp}{{0,1}})'.format(**regex_base)
# regex_base['qchar-JSON-special'] = '(?:{}|:|\{|\}|\[|\])'.format(regex_base['SP'])
# regex_base['charInJSON'] = '(?:{qchar-unescaped}|{qchar-JSON-special}|(?:{escape}(?:{quotation-mark}|{escape}|(?:\/|%2F)|b|f|n|r|t|(?:u{HEXDIG}))))'.format(**regex_base)
# regex_base['stringInJSON'] = '(?:{quotation-mark}{charInJSON}*{quotation-mark})'.format(**regex_base)
# regex_base['primitiveLiteralInJSON'] = '(?:{stringInJSON}|{numberInJSON}|true|false|null)'.format(**regex_base)
# regex_base['value-separator'] = '(?:{BWS}{COMMA}{BWS})'.format(**regex_base)
# regex_base['name-separator'] = '(?:{BWS}{COLON}{BWS})'.format(**regex_base)
# regex_base['begin-array'] = '(?:{0}(?:\[|%5B){0})'.format(regex_base['BWS'])
# regex_base['end-array'] = '(?:{0}(?:\]|%5D){0})'.format(regex_base['BWS'])
# regex_base['begin-object'] = '(?:{0}(?:\{|%7B){0})'.format(regex_base['BWS'])
# regex_base['end-object'] = '(?:{0}(?:\}|%7D){0})'.format(regex_base['BWS'])
# regex_base['keyPropertyValue'] = regex_base['primitiveLiteral']
# regex_base['simpleKey'] = '(?:{OPEN}{keyPropertyValue}{CLOSE})'.format(**regex_base)
# regex_base['keyPropertyAlias'] = regex_base['odataIdentifier']
# regex_base['keyValuePair'] = '(?:(?:{primitiveKeyProperty|keyPropertyAlias}){EQ}{keyPropertyValue})'.format(**regex_base)
# regex_base['compoundKey'] = '(?:{OPEN}{keyValuePair}(?:{COMMA}{keyValuePair})*{CLOSE})'.format(**regex_base)
# regex_base['keyPredicate'] = '(?:{simpleKey}|{compoundKey})'.format(**regex_base)
# regex_base['s']
# regex_base['collectionNavigationExpr'] = ''
# regex_base['propertyPathExpr'] = '(?:{entityColNavigationProperty}{collectionNavigationExpr}{{0,1}})'
# regex_base['memberExpr'] = '(?:({qualifiedEntityTypeName}\/){{0,1}}({propertyPathExpr}|boundFunctionExpr))'
# regex_base['singleNavigationExpr'] = '(?:\/{memberExpr})'
# regex_base['rootExpr'] = '(?:$root/(?:{entitySetName}(?:{keyPredicate}|{singletonEntity}){}{{0,1}}))'

parsing_base = {
    'ALPHA': Word(alphas, exact=1),
    'DIGIT': Word(nums, exact=1),
    'A-to-F': Word(hexnums, exact=1),
    'DQUOTE': Word('%x22', exact=1),
    'SP': Word('%x20', exact=1),
    'HTAB': Word('%x09', exact=1),
    'VCHAR': Word(srange('[%x21-7E]'), exact=1),
    'COLON': Word(':', exact=1),
    'DCOLON': Word(':', exact=2)
}
parsing_base['HEXDIG'] = Word(hexnums, exact=1)
parsing_base['scheme'] = Combine(parsing_base['ALPHA'] + ZeroOrMore(parsing_base['ALPHA'] | parsing_base['DIGIT'] | '+' | '-' | '.'))
parsing_base['port'] = Combine(ZeroOrMore(parsing_base['DIGIT']))
parsing_base['h16'] = Combine(parsing_base['HEXDIG'] + And([Optional(parsing_base['HEXDIG'])]*3))
parsing_base['dec-octet'] = (Combine('1'+And(parsing_base['DIGIT']*2) | ('2' + Word(srange('[%x30-34]'), exact=1)+parsing_base['DIGIT'])|('25'+Word(srange('[%x30-35]'),exact=1))|(Word(srange('[%x31-39]'),exact=1) + parsing_base['DIGIT'])|parsing_base['DIGIT']))
parsing_base['IPv4address'] = Combine(And([parsing_base['dec-octet']+'.']*3) + parsing_base['dec-octet'])
parsing_base['ls32'] = Combine((parsing_base['h16'] + ':' + parsing_base['h16'])|parsing_base['IPv4address'])
parsing_base['IPv6address'] = Combine(
    (And([parsing_base['h16'] + ':']*6) + parsing_base['ls32'])|
    ('::'+And([parsing_base['h16'] + ':']*5) + parsing_base['ls32'])|
    (Optional(parsing_base['h16']) +'::'+And([parsing_base['h16'] + ':']*4) + parsing_base['ls32'])|
    (Optional(Optional(parsing_base['h16'] + ':') + parsing_base['h16']) +'::'+And([parsing_base['h16'] + ':']*3) + parsing_base['ls32'])|
    (Optional(Optional(And([Optional(parsing_base['h16'] + ':')]*2)) + parsing_base['h16']) +'::'+And([parsing_base['h16'] + ':']*2) + parsing_base['ls32'])|
    (Optional(Optional(And([Optional(parsing_base['h16'] + ':')]*3)) + parsing_base['h16']) +'::'+ (parsing_base['h16'] + ':') + parsing_base['ls32'])|
    (Optional(Optional(And([Optional(parsing_base['h16'] + ':')]*4)) + parsing_base['h16']) +'::'+ parsing_base['ls32'])|
    (Optional(Optional(And([Optional(parsing_base['h16'] + ':')]*5)) + parsing_base['h16']) +'::'+ parsing_base['h16'])|
    (Optional(Optional(And([Optional(parsing_base['h16'] + ':')]*6)) + parsing_base['h16']) +'::')
            )
a = Optional(Optional(And([Optional(parsing_base['h16'] + ':')]*6)) + parsing_base['h16']) + '::'
b = ((parsing_base['h16'] + parsing_base['COLON'])*(0,6))*(0,1) + parsing_base['h16'] + parsing_base['DCOLON']
hexdig = Word(hexnums, exact=1)
h16 = Combine(hexdig + And([Optional(hexdig)]*4))
ipv6 = Optional(Optional(And([Optional(h16 + Literal(':'))]*6)) + FollowedBy(h16)) + FollowedBy(Literal('::'))
print ipv6.parseString('ABAF::')
test = Optional(Optional(And([Optional(h16 + ':')]*6)) + h16)
print test.parseString('ABAF')
print a.parseString('::')

debug.set_trace()