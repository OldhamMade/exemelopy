import cgi
import re
from uuid import UUID 

from lxml import etree

class XMLEncoder(object):

    _is_uuid = re.compile(r'^\{?([0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12})\}?$', re.I)

    def __init__(self, data, doc_el='document', encoding='UTF-8', **params):
        self.data = data
        self.document = etree.Element(doc_el, **params)
        self.encoding = encoding

    
    def to_string(self, indent=True, declaration=True):
        xml = self.to_xml()
        if indent:
            self._indent(xml)
        output = etree.tostring(xml, encoding=self.encoding, xml_declaration=declaration)
        return output


    def to_xml(self):
        if self.data:
            self.document = self._update_document(self.document, self.data)
        return self.document


    def from_string(self, string):
        self.document = etree.parse(StringIO(string))
            

    def _update_document(self, node, data):

        if isinstance(data, bool) and data is True:
            node.set('nodetype', u'boolean')
            node.text = u"true"

        elif isinstance(data, bool) and data is False:
            node.set('nodetype', u'boolean')
            node.text = u"false"
        
        elif isinstance(data, basestring) and \
             len(data) in (36, 38) and \
             self._is_uuid.match(data):

            try:
                UUID(data)
            except:
                pass
            else:
                node.set('nodetype', u'uuid')
            finally:
                node.text = self._to_unicode(data)

        elif hasattr(data, 'isoformat'):
            try:
                node.text = data.isoformat()
                node.set('nodetype', u'timestamp')
            except TypeError:
                pass

        elif data is None:
            node.text = None

        elif self._is_scalar(data):
            node.text = self._to_unicode(data)

        elif hasattr(data, 'iteritems'):
            #node.set('nodetype',u'map')
            for name, items in data.iteritems():
                if isinstance(name, basestring) and name != '' and str(name[0]) is '?':
                    #  processing instruction 
                    #self._add_processing_instruction(node, items)
                    pass

                elif isinstance(name, basestring) and name != '' and str(name[0]) is '!':
                    # doctype 
                    #self._add_docype(node, items)
                    pass
                
                    
                elif isinstance(name, basestring) and name != '' and not name[0].isalpha():
                    child = etree.SubElement(node, u'node', name=unicode(name))
                    
                elif isinstance(name, basestring) and name != '':
                    child = etree.SubElement(node, unicode(name))

                else:
                    child = etree.SubElement(node, u"node", name=unicode(name))

                child = self._update_document(child, items)
        
        elif isinstance(data, list):
            node.set('nodetype',u'list')
            for item in data:
                child = etree.SubElement(node, u'i')
                child = self._update_document(child, item)

        elif isinstance(data, set):
            node.set('nodetype',u'unique-list')
            for item in data:
                child = etree.SubElement(node, u'i')
                child = self._update_document(child, item)

        elif hasattr(data, 'send'):
            # generator
            node.set('nodetype',u'generated-list')
            for item in data:
                child = etree.SubElement(node, u'i')
                child = self._update_document(child, item)

        elif isinstance(data, tuple):
            node.set('nodetype',u'fixed-list')
            for item in data:
                child = etree.SubElement(node, u'i')
                child = self._update_document(child, item)

        elif isinstance(data, object):
            children = []
            
            if hasattr(data, '__dict__'):
                children = ((n, v) for n, v in data.__dict__.iteritems() if n[0] is not '_' and not hasattr(n, '__call__'))
                
            if hasattr(data, '__slots__'):
                children = ((n, getattr(data, n)) for n in data.__slots__ if n[0] is not '_' and not hasattr(n, '__call__'))

            sub = etree.SubElement(node, unicode(data.__class__.__name__), nodetype="container")

            for item, value in children:
                child = etree.SubElement(sub, unicode(item))
                child = self._update_document(child, value)

        else:
            raise Exception('self._update_document: unsupported type "%s"' % type(data))

        return node


    def _is_scalar(self, value):
        return isinstance(value, (basestring, float, int, long))
    

    def _indent(self, elem, level=0):
        i = "\n" + "  "*level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


    def _to_unicode(self, string):
        if not string and not self._is_scalar(string):
            return u''
        return unicode(self.escape(string))


    def _add_processing_instruction(self, node, data):

        self.document = etree.ElementTree(self.document)
        
        attrs = []

        if type(data) is dict:
            attrs = self.__dict_to_attrs(dict( (name, value) for name, value in data.iteritems() if name[0].isalpha() and type(value) is not dict  ))

        #pi = etree.ProcessingInstruction(node[1:])#, ' '.join(attrs))
        pi = etree.ProcessingInstruction('xml-stylesheet', 'type="text/xml" href="default.xsl"')

    
    def __dict_to_attrs(self, d):
        return (str(name) + '="' + str(value) + '"' for name, value in d.iteritems())


    def escape(self, data):
        if data is None:
            return None

        if isinstance(data, unicode):
            return data
            #return str(self.unicodeToHTMLEntities(data))
        elif isinstance(data, str):
            try:
                data = unicode(data, 'latin1')
            except:
                pass
            return data
            #return str(self.unicodeToHTMLEntities(data))
        else:
            return data
            #return str(self.unicodeToHTMLEntities(str(data)))


    def unicodeToHTMLEntities(self, text):
        """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
        text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
        #text = text.encode('ascii', 'xmlcharrefreplace')
        #text = cgi.escape(text).encode('UTF-8', 'xmlcharrefreplace')
        return text
