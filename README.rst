=========
exemelopy
=========

exemelopy aims to be a small, light-weight tool for building an XML 
document from native Python data-types without any intervention; an 
XML-version of the json_ and simplejson_ modules.

-----
USAGE
-----

::

    from exemelopy import XMLEncoder
    xml = XMLEncoder({'a': 1, 'b': True, 'spam': 'eggs'}).to_string()
    print xml

Which will return the following output::

    <?xml version='1.0' encoding='UTF-8'?>
    <document>
      <a>1</a>
      <b nodetype="boolean">true</b>
      <spam>eggs</spam>
    </document>

.. _simplejson: http://simplejson.readthedocs.org/
.. _json: http://docs.python.org/library/json.html