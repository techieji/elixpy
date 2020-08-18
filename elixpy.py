"A set of modules which emulate the standard library of Elixir in Python."

__version__ = '0.0.2'

import time
import math
import operator
from inspect import signature
import random

class func:
    "A container for functions which follow the functional programming paradigm."
    class msg:
        "A way to raise errors without terminating the program. Not yet complete."
        ok = True
        error = False
        def __init__(self, msg, value):
            self.msg = msg
            self.value = value
        def __str__(self):
            return (self.msg, self.value).__str__()
        def __repr__(self):
            return (self.msg, self.value).__repr__()
        def nofail(function):
            "Create a function which doesn't fail when it raises an error."
            def f(*args, **kwargs):
                try:
                    return func.msg(func.msg.ok, function(*args, **kwargs))
                except Exception as e:
                    return func.msg(func.msg.error, e)
            return f
    class thunk:
        "A class used for partial function application and deferring function calls"
        def __init__(self, func: callable, *args, **kwargs):
            self.func = func
            self.args = args
            self.kwargs = kwargs
            self.num = len(signature(func).parameters)
        def __call__(self, *args, **kwargs):
            num = len(self.args) + len(args) + len(self.kwargs) + len(kwargs) 
            if num == self.num:
                return self.func(*self.args, *args, **self.kwargs, **kwargs)
            elif num < self.num:
                return func.thunk(self, *self.args, *args, **self.kwargs, **kwargs)
            else:
                raise TypeError(f"Exactly {self.num} arguments are needed ({num} given)")
    class enum(list):
        "A container for eager functions which work with enumerables."
        def pipe(self, fn, *args, **kwargs):
            return fn(self, *args, **kwargs)
        def chunk_by(i, fn):
            """
            Returns an enumerable which contains sublists. These sublists all
            contain values which when passed into the function, produce the
            same result. Order is preserved. An example:
                >>> func.enum.chunk_by([0, 1, 2, -1, -2], lambda x: x > 0)
                [[0], [1, 2], [-1, -2]]
            """
            i = iter(i)
            ans = [[next(i)]]
            for x in i:
                lastres = fn(ans[-1][0])
                if fn(x) != lastres:
                    ans.append([])
                ans[-1].append(x)
            return ans
        def dedup_by(i, fn):
            """
            Deletes duplicates with a function. The function maps a value to 
            another value which can be used to determine if two values are
            different. Does not mutate the original enumerable. An example:
                >>> func.enum.dedup_by([1, 2, 3, 4], lambda x: x % 2)
                [1, 2]
            """
            fncalls = set()
            ret = []
            for x in i:
                if fn(x) not in fncalls:
                    fncalls.add(fn(x))
                    ret.append(x)
            return ret
        def dedup(i):
            """
            Deletes duplicates. Does not mutate the original enumerable.
            An example:
                >>> func.enum.dedup([1, 1, 2, 2, 3, 5, 3])
                [1, 2, 3, 5]
            """
            return func.enum.dedup_by(i, lambda x: x)
        def rotate(l: list, shift: int = 1) -> iter:
            """
            Rotates all the elements in an enumerable by the specified shift. 
            The shift defaults to 1. Some examples:
                >>> func.enum.rotate([1, 2, 3, 4])
                [4, 1, 2, 3]
                >>> func.enum.rotate([1, 2, 3, 4], shift=2)
                [3, 4, 1, 2]
                >>> func.enum.rotate([1, 2, 3, 4], shift=-1)
                [2, 3, 4, 1]
            """
            return l[-shift:] + l[:-shift]
        def find(l: list, index: int) -> object:
            """
            Indexes into a enumerable. For a list, is equivalent to l[i]. This
            function works with any enumerable. An example:
                >>> func.enum.find([1, 3, 2, 4], 1)
                3
            """
            l = iter(l)
            while index:
                next(l)
                index -= 1
            return next(l)
        def flip(l: list, i1: int, i2: int = None) -> list:
            """
            Replaces two element of a list with each other. The second index
            defaults to the first index plus one. Some examples:
                >>> func.enum.flip([1, 2, 3, 4], 1, 2)
                [1, 3, 2, 4]
                >>> func.enum.flip([1, 2, 3, 4], 1)
                [1, 3, 2, 4]
            """
            if i2 == None:
                i2 = i1 + 1
            i1, i2 = sorted([i1, i2])
            t = type(l)
            return l[:i1] + t([l[i2]]) + l[i1 + 1:i2] + t([l[i1]]) + l[i2 + 1:]
        def map(l: iter, fn: callable) -> iter:
            """
            Maps a function over an enumerable. Is eager and does not accept
            more than one enumerable. Note: the built-in map is a lazy version.
            An example:
                >>> func.enum.map([1, 2, 3, 4], lambda x: x + 2)
                [3, 4, 5, 6]
            """
            return type(l)([fn(x) for x in l])
        def flatmap(fn: callable, *ls) -> iter:
            """
            Maps a function over an enumerable and then flattens the result.
            Accepts multiple enumerables as arguments. Some examples:
                >>> fun = lambda x: (x, -x)
                >>> func.enum.flatmap(fun, [1, 2, 3])
                [1, -1, 2, -2, 3, -3]
                >>> fun = lambda x, y: (x + y, x - y)
                >>> func.enum.flatmap(fun, [1, 2, 3], [3, 2, 1])
                [4, -2, 4, 0, 4, 2]
            """
            ret = []
            for x in zip(*ls):
                try:
                    ret += list(fn(*x))
                except TypeError:
                    ret += [fn(*x)]
            return type(ls[0])(ret)
        def filter(fn: callable, l: iter) -> iter:
            """
            Eager variation of the built-in function `filter`. An example:
                >>> func.enum.filter(lambda x: x > 0, [-2, -1, 0, 1, 2])
                [1, 2]
            """
            return type(l)([x for x in l if fn(x)])
        def flatten(l) -> iter:
            """
            Flattens a list one level. Some examples:
                >>> func.enum.flatten([[1, 2], [3, 4, 5]])
                [1, 2, 3, 4, 5]
            """
            return func.enum.flatmap(lambda x: x, l)
        def foldr(f: callable, acc: object, l: iter) -> object:
            """
            Folds the given enumerable rightward with the given accumulator and
            given function. An example:
                >>> func.enum.foldr(lambda x, y: x - y, 0, range(1, 11))
                -5
            """
            if len(l) == 1:
                return f(l[0], acc)
            else:
                return f(l[0], func.enum.foldr(f, acc, l[1:]))
        def foldl(f: callable, acc: object, l: iter) -> object:
            """
            Folds the given enumerable leftward with the given accumulator and
            given function. An example:
                >>> func.enum.foldl(lambda x, y: x - y, 0, range(1, 11))
                -55
            """
            for x in l[::-1]:
                acc = f(acc, x)
            return acc
        def reject(fn: callable, l: iter) -> iter:
            """
            Filters out the elements in the enumerable for which the function
            returns `True`. An example:
                >>> func.enum.reject(lambda x: x > 0, [-2, -1, 0, 1, 2])
                [-2, -1, 0]
            """
            return func.enum.filter(lambda x: not(fn(x)), l)
        def scanr(f: callable, acc: object, l: iter) -> iter:
            def fn(x, acc):
                return acc + [f(acc, x)]
            return func.enum.foldr(fn, acc, l)
        def scanl(f: callable, acc: object, l: iter) -> iter:
            def fn(x, acc):
                return acc + [f(acc, x)]
            return func.enum.foldl(fn, acc, l)
        def zip(*ls):
            """
            Eager version of the built-in function `zip`. An example:
                >>> func.enum.zip([1, 2, 3], [3, 2, 1])
                [(1, 3), (2, 2), (3, 1)]
            """
            return type(ls[0])(zip(*ls))
        def unzip(e: iter):
            """
            Unzips a zipped enumerable. Returns a list of lists containing the
            original lists. An example:
                >>> z = zip([1, 2, 3], [3, 2, 1])
                >>> func.enum.unzip(z)
                [[1, 2, 3], [3, 2, 1]]
            """
            e = list(e)
            ret = [[] for x in range(len(e[0]))]
            for x in e:
                for i in range(0, len(x)):
                    ret[i].append(x[i])
            return ret
        def take(e: iter, num: int):
            """
            Takes the first `num` elements from the given enumerable.
            For lists, equivalent to l[0:n - 1]. An example:
                >>> func.enum.take([1, 2, 3, 4, 5], 2)
                [1, 2]
            """
            e = iter(e)
            i = 0
            l = []
            for x in e:
                if i == num:
                    break
                l.append(x)
                i += 1
            return l
    class stream:
        """
        A class for dealing with large, possibly infinite collections. Note
        that this class has much more support for infinite collections than
        finite ones. Can be initalized with a rule or with one of the functions
        which return a stream as a result. Streams are lazy and thus defer
        operations until needing to do them. This means that streams need to
        iterate over all the elements only once. Streams are a good choice when
        you need to do many operations on a large set of data.
        """
        def __init__(self, rule: callable):
            """
            Takes a callable to initalize. The callable takes one argument, the
            index and returns the element at that index.
            """
            self.rule = rule
            self.i = -1
            self.iter = self
        def __next__(self):
            self.i += 1
            return self.rule(self.i)
        def __iter__(self):
            self.i = -1
            return self
        def pipe(self, fun, *args, **kwargs):
            return fun(self, *args, **kwargs)
        def find(s, i):
            """
            Locates the element of the given stream at the specified index.
            An example:
                >>> s = func.stream(lambda x: x + 1)
                >>> func.stream.find(s, 5)
                6
            """
            return s.rule(i)
        def from_iter(it: iter):
            """
            Converts an enumerable into a stream. Any values beyond the final
            element of the enumerable will be given as None.
            """
            def f(i):
                x = list(it)
                index = 0
                try:
                    return x[i]
                except IndexError:
                    return None
            ret = func.stream(f)
            ret.iter = it
            return ret
        def chunk_by(s: iter, fn: callable):
            """
            Takes a stream and a callable and returns a stream which emits
            chunks for which the result of the function called on them is the
            same. See the doc string of func.enum.chunk_by.
            """
            def f(i):
                enumed = []
                index = 1
                while len(enumed) < i + 1:
                    enumed = func.enum.chunk_by(func.enum.take(s, index), fn)
                    index += 1
                return enumed[-2]
            return func.stream(f)
        def concat(s1, s2):
            """
            Joins two streams together. It's lazy, like all other functions in
            this module, so if the first stream is infinite, nothing will
            happen. Isn't implemented correctly.
            """
            raise NotImplementedError
            def f(i):
                if func.stream.find(s1, i) == None:
                    return func.stream.find(s2, i)
                else:
                    return func.stream.find(s1, i)
            return func.stream(f)
        def cycle(it):
            """
            Cycles through an enumerable. For example, cycling over [1, 2, 3]
            will produce the stream [1, 2, 3, 1, 2, 3, 1, ...]. An example:
                >>> s = func.stream.cycle([1, 2, 3])
                >>> func.enum.find(s, 5)
                3
            """
            it = func.stream.from_iter(it)
            def f(i):
                return func.stream.find(it, i % len(it.iter))
            return func.stream(f)
        def dedup_by(it, fn):
            """
            Returns a stream which only emits elements if they are different
            from the last element according to the transformation function
            given. See the doc string for func.enum.dedup_by
            """
            last = None
            offset = 0
            def f(i):
                while fn(func.stream.find(it, i + offset)) == last:
                    offset += 1
                ret = func.stream.find(it, i + offset)
                last = fn(ret)
                return ret
            return func.stream(f)
        def dedup(it):
            "See the doc string for func.enum.dedup"
            return func.stream.dedup_by(it, lambda x: x)
        def map(s, fn):
            """
            A lazy map. Note that this function provides exactly the same
            functionality as the built-in map function.
            """
            def f(i):
                return fn(s.rule(i))
            return func.stream(f)
        def iterate(start, fn):     # look at the memory constant impl
            """
            Repeatedly applies the given function i times to the starting value
            to get the i-th element. Produces a string. Note: this isn't
            implemented correctly yet.
            """
            raise NotImplementedError
            def f(i):
                func = lambda x: x
                for x in range(i):
                    func = lambda x: fn(func(x))
                return func(i)
            return func.stream(f)
    def protocol(*functions) -> callable:
        """
        A decorator which delegates to other function by using the types of the
        argument. When no function matches, calls the code in the decorated 
        function. Make sure that the function is annotated.  
        """
        def dec(function) -> callable:
            def f(*args):
                types = list(map(type, args))
                for func in functions:
                    if list(func.__annotations__.values()) == types:
                        return func(*args)
                return function(*args)
            return f
        return dec
    def guard(condition: callable, default = None) -> callable:
        """
        Decorator which calls the function only if the condition is satisfied.
        Otherwise, it defaults to default, which defaults to None.
        """
        def dec(f: callable) -> callable:
            class F:
                guardcon = condition
                def __call__(self, *args, **kwargs):
                    if condition(*args, **kwargs):
                        return f(*args, **kwargs)
                    else:
                        return default
            return F()
        return dec
    def compose(*functions) -> callable:
        """
        Composes the functions given. Is not robust. Use at your own risk.
        """
        def f(*args, **kwargs):
            if len(functions) == 1:
                return functions[0](*args, **kwargs)
            else:
                return functions[0](func.compose(*functions[1:])(*args, **kwargs))
        return f
    def argoverload(*functions) -> callable:
        """
        Decorator which calls a different function based off of the numer of
        arguments given. If nothing matches, calls the decorated function.
        """
        def dec(function) -> callable:
            def f(*args, **kwargs):
                for x in functions:
                    if len(signature(x).parameters) == len(args) + len(kwargs):
                        return x(*args)
                return function(*args)
            return f
        return dec
    def memoize(size: int = None) -> callable:
        """
        A simple memoizer. Saves already called function calls in order to
        speed up future function calls. Saves up to `size` entries.
        """
        def dec(function: callable) -> callable:
            d = {}
            def f(*args, **kwargs):
                if size and len(d) > size - 1:
                    del d[random.choice(d)]
                if args not in d.keys():
                    d[args] = function(*args, **kwargs)
                return d[args]
            return f
        return dec
    def rotateargs(function: callable, shift: int = 1):
        """
        Rotates the arguments given. For example, if there exists a function
        `f(a, b, c)` will be turned into `lambda a, b, c: f(c, a, b).
        """
        def f(*args, **kwargs):
            return function(*func.enum.rotate(args, shift), **kwargs)
        return f
    def flipargs(function: callable, i1: int = 0, i2: int = None) -> callable:
        """
        Flips the specified arguments of the function.
        """
        def f(*args, **kwargs):
            return function(*func.enum.flip(args, i1, i2), **kwargs)
        return f
    def match(tree: list, values: list) -> dict:
        """
        A pattern matching tool for Python. Can be used to destructure complex
        data structure when you know the structure of the data. An example:
            >>> func.match(['a', ('b', 'c')], [1, (2, 3)])
            {'a': 1, 'b': 2, 'c': 3}
        """
        d = {}
        for t, v in zip(tree, values):
            if hasattr(t, '__iter__') and type(t) == type(v):
                d.update(func.match(t, v))
            else:
                d[t] = v
        return d
