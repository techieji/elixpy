# Enumerables

Enumerables, known in Python as iterables, are basically items which can be enumerated. The functions in this class are all eager, meaning that they immediately execute themselves on the enumerable. An example of a lazy function is the built-in map function, which only evaluates the function when iterated. Most functions in this class are taken from Elixir's standard library. This section assumes that you have imported it like so: `from elixpy import func`. None of these functions mutate the arguments given.

## Enum

`func.enum(iterable)`

The `enum` class is identical to the list except for the fact that it has a pipe method which can be used to chain multiple functions together.

### Pipe

`func.enum.pipe(self, function, *args, **kwargs)`

Pipe is the only method of `func.enum`. It allows you to chain multiple functions together. If `e` is an enum, then `e.pipe(func.enum.map, lambda x: x + 1)` is equivalent to `func.enum.map(e, lambda x: x + 1)`.

## Chunk By

`func.enum.chunk_by(enum, chunker)`

`chunk_by` splits an enumerable into sublists such that `chunker` returns the same value for each chunk and in such a way such that flattening the value returned will get the original enumerable. An example is given to illustrate:

```python
>>> e = [-2, -1, 0, 1, 2, 1, 0, -1]
>>> greaterthan0 = lambda x: x > 0
>>> func.enum.chunk_by(e, greaterthan0)
[[-2, -1, 0], [1, 2, 1], [0, -1]]
```

Note that the function given does not need to return a boolean; it just needs to return any value which can be used to differentiate between two different chunks

## Dedup

`func.enum.dedup(enum)`

Deletes repeated elements in the enumerable. Equivalent to converting `enum` to a set.

## Dedup By

`func.enum.dedup_by(enum, func)`

Deletes elements marked as the same by `func` in the enumerable. `func` takes one argument and returns a value which can be used to mark two values as duplicates. For example, to retain all values which have different moduli with 6, you would type `func.enum.dedup_by(enum, lambda x: x % 6)`.

## Rotate

`func.enum.rotate(enum, shift=1)`

Shifts every element in `enum` rightward `shift` elements. That is, `e[i]` will be in `e[i + shift]` after the shift is complete. When the shift is negative, the elements will move left. Here are some examples:

```python
>>> func.enum.rotate([1, 2, 3, 4])
[4, 1, 2, 3]
>>> func.enum.rotate([1, 2, 3, 4], shift=2)
[3, 4, 1, 2]
>>> func.enum.rotate([1, 2, 3, 4], shift=-1)
[2, 3, 4, 1]
```

## Find

`func.enum.find(enum, i)`

Figures out what element is at index `i` in `enum`. When `enum` is a list or a tuple, it is equivalent to `enum[i]`. This works for any iterable. 

## Flip

`func.enum.flip(enum, i1, i2)`

Replaces the elements at `i1` and `i2` in `enum` with each other.

## Map

`func.enum.map(enum, fn)`

Returns an enumerable for which the element at `i` will be `fn(enum[i])`. This function is eager, not lazy as the built-in function is.

## Flatmap

`func.enum.flatmap(enum, fn)`

Returns the flattened result of mapping `fn` over `enum`

## Filter

`func.enum.filter(fn, enum)`

Eager version of the built-in filter.

## Flatten

`func.enum.flatten(enum)`

Flattens `enum` one level.

## Foldr

`func.enum.foldr(fn, acc, enum)`

Folds a list rightward. 

## Foldl

`func.enum.foldl(fn, acc, enum)`

Folds a list leftward.

## Reject

## Scanr

## Scanl

## Zip

## Unzip

`func.enum.unzip(enum)`

Unzips a given enumerable. For example,

```python
>>> l = [(1, 1), (2, 3), (3, 5)]
>>> func.enum.unzip(l)
[[1, 2, 3], [1, 3, 5]]
```

## Take

`func.enum.take(enum, n)`

Takes the first `n` elements of `enum`. For lists, this is equivalent to `enum[:n]`
