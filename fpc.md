# Functional Programming Constructs

This section contains many decorators and functions which take other functions as arguments.

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
