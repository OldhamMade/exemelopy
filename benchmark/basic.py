import os
import sys
import datetime
from collections import MutableMapping as DictMixin
from unitbench import Benchmark

BASE_PATH = '/'.join(os.path.dirname(
    os.path.abspath(__file__)).split('/')[0:-1])

if BASE_PATH not in sys.path:
    sys.path.insert(1, BASE_PATH)

from exemelopy import XMLEncoder


class SimpleObject(object):
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


class BasicBenchmark(Benchmark):

    def input(self):
        return [100]

    def bench_None(self, input_):
        for _ in xrange(input_):
            XMLEncoder(None).to_string()

    def bench_Basic_Integer(self, input_):
        for _ in xrange(input_):
            XMLEncoder(123).to_string()

    def bench_Basic_Float(self, input_):
        for _ in xrange(input_):
            XMLEncoder(1.23).to_string()

    def bench_Basic_String(self, input_):
        for _ in xrange(input_):
            XMLEncoder('simple string').to_string()

    def bench_Basic_List(self, input_):
        for _ in xrange(input_):
            XMLEncoder([1, 2, 3, 4, 5]).to_string()

    def bench_Basic_Set(self, input_):
        for _ in xrange(input_):
            XMLEncoder(set([1, 2, 3, 4, 5])).to_string()

    def bench_Basic_Tuple(self, input_):
        for _ in xrange(input_):
            XMLEncoder((1, 2, 3, 4, 5)).to_string()

    def bench_Basic_Generator(self, input_):
        data = list(range(10))
        for _ in xrange(input_):
            XMLEncoder(data).to_string()

    def bench_Empty_Dict(self, input_):
        for _ in xrange(input_):
            XMLEncoder({}).to_string()

    def bench_Basic_Dict(self, input_):
        for _ in xrange(input_):
            XMLEncoder({'a': 1}).to_string()

    def bench_True(self, input_):
        for _ in xrange(input_):
            XMLEncoder(True).to_string()

    def bench_False(self, input_):
        for _ in xrange(input_):
            XMLEncoder(False).to_string()

    def bench_Simple_Object(self, input_):
        data = SimpleObject()
        for _ in xrange(input_):
            XMLEncoder(data).to_string()

    def bench_Complex_Object(self, input_):
        data = ComplexObject()
        for _ in xrange(input_):
            XMLEncoder(data).to_string()

    def bench_Date_Object(self, input_):
        data = datetime.datetime(2010, 2, 1, 0, 0)
        for _ in xrange(input_):
            XMLEncoder(data).to_string()

    def bench_Large_Object(self, input_):
        data = {}
        for i in xrange(10):
            data[i] = {}
            for j in xrange(10):
                data[i][j] = {
                    'a': list(x for x in xrange(50)),
                    'b': set(x for x in xrange(50)),
                    'c': tuple(x for x in xrange(50)),
                    'd': (x for x in xrange(50)),
                    'e': datetime.datetime.utcnow(),
                    'f': "Hello World " * 500,
                    'g': True,
                    'h': False,
                    'i': None,
                    }

        for _ in xrange(input_):
            XMLEncoder(data).to_string()
