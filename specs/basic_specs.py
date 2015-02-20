from collections import MutableMapping as DictMixin
import datetime
import os
import sys
import tempfile
import unittest

try:
    from io import BytesIO  # python 3
except ImportError:
    from cStringIO import StringIO as BytesIO  # python 2

BASE_PATH = '/'.join(os.path.dirname(
    os.path.abspath(__file__)).split('/')[0:-1])

if BASE_PATH not in sys.path:
    sys.path.insert(1, BASE_PATH)

from exemelopy import *


class PlainObject(object):
    pass


class ComplexObject(DictMixin):
    def __init__(self):
        self.dict = dict()

    def __delitem__(self, key):
        del self.dict[key]

    def __getitem__(self, key):
        return self.get(key, KeyError)

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def __setitem__(self, key, value):
        self.append(key, value)

    def get(self, key, default=None):
        if key not in self.dict:
            return default
        return self.dict[key]


class CommonBaseSpec(unittest.TestCase):
    def _format_each_should_equal(self, items):
        for test, expected in items:
            output = XMLEncoder(test).to_string()
            self.assertEqual(output, expected)


class BasicSpec(CommonBaseSpec):

    def it_should_format_simple_items(self):
        tests = (
            (None, "<?xml version='1.0' encoding='UTF-8'?>\n<document/>\n"),
            ('test', '<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
             '\n<document>test</document>\n'),
            )

        self._format_each_should_equal(tests)

    def it_should_format_lists(self):
        tests = (
            ([1, 2, 3], '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
             '<document nodetype="list">\n  <i>1</i>\n  <i>2</i>\n  '
             '<i>3</i>\n</document>\n'),
            )

        self._format_each_should_equal(tests)

    def it_should_format_sets(self):
        tests = (
            (set([1, 2, 3]), '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
             '<document nodetype="unique-list">\n  <i>1</i>\n  <i>2</i>\n  '
             '<i>3</i>\n</document>\n'),
            )

        self._format_each_should_equal(tests)

    def it_should_format_integer_keys(self):
        tests = (({
            1: 1,
            2: 2,
            3: 3,
            }, '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<document>\n  '
            '<node name="1">1</node>\n  <node name="2">2</node>\n  '
            '<node name="3">3</node>\n</document>\n'),)

        self._format_each_should_equal(tests)

    def it_should_format_tuples(self):
        tests = (
            ((1, 2, 3), '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
             '<document nodetype="fixed-list">\n  <i>1</i>\n  <i>2</i>\n  '
             '<i>3</i>\n</document>\n'),
            )

        self._format_each_should_equal(tests)

    def it_should_format_nested_unicode_dicts(self):
        tests = (
            ({u'foo': u'bar'},
             '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<document>\n  '
             '<foo>bar</foo>\n</document>\n'),
            ({u'foo': {u'bar': u'baz'}}, '<?xml version=\'1.0\' '
             'encoding=\'UTF-8\'?>\n<document>\n  <foo>\n    <bar>baz</bar>'
             '\n  </foo>\n</document>\n'),
            ({u'packages': [],
              u'terms': None,
              u'description': {
                  u'short': u'sldf',
                  u'long': u'skdjhfskjfdgn'
                  },
              u'title': u'meh',
              u'expires': datetime.datetime(2010, 2, 1, 0, 0),
              u'venues': [],
              u'activity': None,
              u'_id': '4d2596f7fa5bd80e18000001',
              u'type': None
              },
             """<?xml version='1.0' encoding='UTF-8'?>
<document>
  <activity/>
  <expires nodetype="timestamp">2010-02-01T00:00:00</expires>
  <terms/>
  <description>
    <short>sldf</short>
    <long>skdjhfskjfdgn</long>
  </description>
  <title>meh</title>
  <packages nodetype="list"/>
  <type/>
  <venues nodetype="list"/>
  <node name="_id">4d2596f7fa5bd80e18000001</node>
</document>
"""),
            )

        self._format_each_should_equal(tests)

    def it_should_format_special_characters(self):
        tests = (
            ('< & >', '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'
             '<document>&lt; &amp; &gt;</document>\n'),
            )

        self._format_each_should_equal(tests)

    def it_should_format_newlines_correctly(self):
        tests = (
            ('''This

is

a

long

paragraph

''', '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<document>This

is

a

long

paragraph

</document>
'''),
            (('''This

is

a''', '''

long

paragraph

'''), '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<document \
nodetype="fixed-list">
  <i>This

is

a</i>
  <i>

long

paragraph

</i>
</document>
'''),
            )

        self._format_each_should_equal(tests)


class ObjectSpec(CommonBaseSpec):

    def it_should_format_generator_objects(self):
        tests = (
            ((i for i in xrange(1,4)), '<?xml version=\'1.0\' '
             'encoding=\'UTF-8\'?>\n<document nodetype="generated-list">\n  '
             '<i>1</i>\n  <i>2</i>\n  <i>3</i>\n</document>\n'),
            )

        self._format_each_should_equal(tests)

    def it_should_format_complex_objects(self):

        nesteddict = {
            'foo': set([1,2,3]),
            'bar': False,
            'baz': {
                'a': (1,2,3),
                'b': datetime.date(2002, 3, 11),
                'c': "{36980915-cd66-4547-9081-760ad0d77625}"
                }
            }

        test_object = PlainObject()
        test_object.bar = 'baz'
        test_object.nested = nesteddict

        titles = {
            'long title': 'some text',
        }

        tests = (
            ((1, 2, 3), '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<document nodetype="fixed-list">
  <i>1</i>
  <i>2</i>
  <i>3</i>
</document>
'''),
            (['foo', 'bar', True],
             '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<document nodetype="list">
  <i>foo</i>
  <i>bar</i>
  <i nodetype="boolean">true</i>
</document>
'''),
            ((i for i in [1, 2, 3]),
             '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<document nodetype="generated-list">
  <i>1</i>
  <i>2</i>
  <i>3</i>
</document>
'''),
            (nesteddict,
             '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<document>
  <baz>
    <a nodetype="fixed-list">
      <i>1</i>
      <i>2</i>
      <i>3</i>
    </a>
    <c nodetype="uuid">{36980915-cd66-4547-9081-760ad0d77625}</c>
    <b nodetype="timestamp">2002-03-11</b>
  </baz>
  <foo nodetype="unique-list">
    <i>1</i>
    <i>2</i>
    <i>3</i>
  </foo>
  <bar nodetype="boolean">false</bar>
</document>
'''),
            (footest_object,
             '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<document>
  <PlainObject nodetype="container">
    <bar>baz</bar>
    <nested>
      <baz>
        <a nodetype="fixed-list">
          <i>1</i>
          <i>2</i>
          <i>3</i>
        </a>
        <c nodetype="uuid">{36980915-cd66-4547-9081-760ad0d77625}</c>
        <b nodetype="timestamp">2002-03-11</b>
      </baz>
      <foo nodetype="unique-list">
        <i>1</i>
        <i>2</i>
        <i>3</i>
      </foo>
      <bar nodetype="boolean">false</bar>
    </nested>
  </PlainObject>
</document>
'''),
            (titles,
             '''<?xml version=\'1.0\' encoding=\'UTF-8\'?>
<document>
  <node name="long title">some text</node>
</document>
'''),
            )

        self._format_each_should_equal(tests)

    def it_should_format_io_objects(self):
        tests = (
            ({'data': BytesIO('this is some data')},
             "<?xml version='1.0' encoding='UTF-8'?>\n<document>\n  "
             "<data>this is some data</data>\n</document>\n"),
            )

        self._format_each_should_equal(tests)


class UnsupportedFormatSpec(CommonBaseSpec):

    def it_should_raise_for_unsupported_formats(self):
        data = {
            'file': tempfile.TemporaryFile()
            }

        self.assertRaises(
            TypeError,
            XMLEncoder(data, strict_errors=True).to_string)

    def it_should_skip_errors(self):
        """it should not raise on skip_errors"""
        tests = (
            ({'file': tempfile.TemporaryFile()},
             '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<document>\n  '
             '<file nodetype="unsupported-type">&lt;type \'file\'&gt;</file>'
             '\n</document>\n'),
            )

        self._format_each_should_equal(tests)
