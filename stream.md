# Streams

Streams are iterables which are used when you are dealing with large, possibly infinite data. Streams are preferred over normal iterables like `list` and `tuple` because streams only need to make one pass over itself in order to update it. Enums behave as follows:

```python
def myprint(x):
    print(x)
    return x
    
>>> e = func.enum([1, 2, 3])
>>> (e.pipe(func.enum.map, myprint)
      .pipe(func.enum.map, lambda x: x * 2)
      .pipe(func.enum.map, myprint))
1
2
3
2
4
6
[2, 4, 6]
```

Streams, on the other hand, behave like so:

```python
def myprint(x):
    print(x)
    return x
    
>>> s = func.stream(lambda x: x)
>>> new_s = (s.pipe(func.stream.map, myprint)
              .pipe(func.stream.map, lambda x: x * 2)
              .pipe(func.stream.map, myprint))
```

Nothing is printed. This is because streams only evaluate themselves when an eager function is applied:

```python
>>> func.enum.take(new_s, 3)
1
2
2
4
3
6
[2, 4, 6]
```

Note that the order is different. This is because the stream is making only one pass; it evaluates all the functions on a single element before moving on to the next one. This makes streams a very efficient iterable.
