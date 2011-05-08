import os, sys
import datetime
from collections import MutableMapping as DictMixin
from unitbench import Benchmark

BASE_PATH = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[0:-1])

if BASE_PATH not in sys.path:
    sys.path.insert(1, BASE_PATH)

from exemelopy import XMLEncoder

class SimpleObject(object):
    pass

class ComplexObject(DictMixin):
    def __init__(self): self.dict = dict()
    def __delitem__(self, key): del self.dict[key]
    def __getitem__(self, key): return self.get(key, KeyError)
    def __iter__(self): return iter(self.dict)
    def __len__(self): return len(self.dict)
    def __setitem__(self, key, value): self.append(key, value)

    def get(self, key, default=None):
        if key not in self.dict:
            return default
        return self.dict[key]


class BasicBenchmark(Benchmark):

    def input(self):
        return [1000]

    def bench_None(self, input):
        for i in xrange(input):
            output = XMLEncoder(None).to_string()

    def bench_Basic_Integer(self, input):
        for i in xrange(input):
            output = XMLEncoder(123).to_string()

    def bench_Basic_Float(self, input):
        for i in xrange(input):
            output = XMLEncoder(1.23).to_string()

    def bench_Basic_String(self, input):
        for i in xrange(input):
            output = XMLEncoder('simple string').to_string()

    def bench_Basic_List(self, input):
        for i in xrange(input):
            output = XMLEncoder([1,2,3,4,5]).to_string()

    def bench_Basic_Set(self, input):
        for i in xrange(input):
            output = XMLEncoder(set([1,2,3,4,5])).to_string()

    def bench_Basic_Tuple(self, input):
        for i in xrange(input):
            output = XMLEncoder((1,2,3,4,5)).to_string()

    def bench_Basic_Generator(self, input):
        data = (i for i in xrange(10))
        for i in xrange(input):
            output = XMLEncoder(data).to_string()

    def bench_Empty_Dict(self, input):
        for i in xrange(input):
            output = XMLEncoder({}).to_string()

    def bench_Basic_Dict(self, input):
        for i in xrange(input):
            output = XMLEncoder({'a':1}).to_string()

    def bench_True(self, input):
        for i in xrange(input):
            output = XMLEncoder(True).to_string()

    def bench_False(self, input):
        for i in xrange(input):
            output = XMLEncoder(False).to_string()

    def bench_Simple_Object(self, input):
        data = SimpleObject()
        for i in xrange(input):
            output = XMLEncoder(data).to_string()

    def bench_Complex_Object(self, input):
        data = ComplexObject()
        for i in xrange(input):
            output = XMLEncoder(data).to_string()

    def bench_Date_Object(self, input):
        data = datetime.datetime(2010, 2, 1, 0, 0)
        for i in xrange(input):
            output = XMLEncoder(data).to_string()

    '''
    def bench_Large_Object(self, input):
        data = {}
        for i in xrange(20):
            data[i] = {}
            for j in xrange(20):
                data[i][j] = {
                    
                    }
        for i in xrange(input):
            output = XMLEncoder(data).to_string()
    '''
