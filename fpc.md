# Functional Programming Constructs

This section contains many decorators and functions which take other functions as arguments. This section assumes that elixpy has been imported like so: `from elixpy import func`.

## Protocol

    `@protocol(*functions)`
 
`protocol` allows you to overload functions based on type and number of arguments. For example,
let us define an add function which can add integers or strings:

```python
        
def addint(x: int, y: int):
    print(f"Adding integers {x} and {y}")
    return x + y
            
def addstr(x: str, y: str):
    print(f"Adding strings {x} and {y}")
    return x + y
        
@func.protocol(addint, addstr)
def add(*args):
    print(f"I do not know how to interpret {args}")
```

Let's see how `add` reacts to different arguments:

```python
>>> add(1, 2)
Adding integers 1 and 2
3
>>> add("x", "y")
Adding strings x and y
'xy'
>>> add(4.0, 5.0)
I do not know how to interpret (4.0, 5.0)
```

In order for `func.protocol` to work, the functions must have _annotations_. Note that the return type shouldn't be indicated.

## Guard

    `@func.guard(condition, default=None)`
    
This decorator allows you to impose a guard condition. The condition function takes the arguments given to the function and returns a boolean. If the condition returns `True`, it calls the function which was decorated. Otherwise, it returns the default.

```python
@func.guard(condition, default)
def f(*args, *kwargs):
    # Do something
    pass
```

is equivalent to

```python
def f(*args, **kwargs):
    if condition(*args, **kwargs):
        return default
    else:
        # Do something
        pass
```

The decorated function has the attribute `guardcon` which returns the condition.

## Compose

Implementation is not yet robust.

## Argoverload

## Memoize

    `func.memoize(size = 1000)`
    
A simple memoizer. Memoization is a common optimization which works by storing previously called function calls. This is very helpful on tree recursive or even just normal recursive functions. On my computer, when `purefib` and `fastfib` is implemented like so,

```python
def purefib(n):
    if n < 2:
        return 1
    else:
        return purefib(n - 1) + purefib(n - 2)
        
@func.memoize(10000)
def fastfib(n):
    if n < 2:
        return 1
    else:
        return fastfib(n - 1) + fastfib(n - 2)
```

`purefib(40)` takes 98.5749020576477 seconds to complete while `fastfib(40)` takes 9.989738464355469e-05 seconds to complete.

## Match

    `func.match(tree, value)`
    
Sometimes, you know what you want from a data structure but it's hard to do it. That is what pattern matching is for. 
