# Echo Parser


## Usage

Because of the way command line arguments are parsed, wrap the expression around quotes. For example:

```
$ python3 echo.py 'a{b,c}'
```

Alternatively:

```
$ chmod u+x echo.py
$ ./echo.py 'a{b,c}'
```

Or from the Python shell:
```python
>>> from echo import parse
>>> parse('a{b,c}')
```

## Tests

```
$ python3 -m unittest tests
```

## Additional Info

Python 2 is also supported.
