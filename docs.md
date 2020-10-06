Module datastructure
--------------------
Thin wrapper around `dict` or `list` that provides easy access to nested datastructures
that may contain lists, dicts and simple types.

Values can be accessed via a path notation (default: dot-separated).

Supports getting, modifying, appending and removing values from the nested data structure,
iteration over a path pattern and `in` (contains) operation for paths.

Supports either "silent mode", where trying to access non-existing data just returns None,
or can throw KeyError of any of the items along the path does not exist.

Does NOT create a copy of the data structure, which can be very handy for processing existing
complex data (e.g. parsed JSON value).

For more details see the doctests below.

## Usage:

### List based data structures

    >>> import json
    >>> _show_as_string = lambda value: json.dumps(value.data if isinstance(value, Datastructure) else value , sort_keys=True, ensure_ascii=False)

    >>> l = Datastructure([
    ...     {
    ...         "name": "Peter",
    ...         "age": 45,
    ...     },
    ...     {
    ...         "name": "John",
    ...         "age": 13,
    ...         "friends": [
    ...             "Betty",
    ...             {
    ...                 "name": "Lucy",
    ...                 "since": '1999',
    ...             },
    ...         ]
    ...     },
    ... ],
    ... silent_fail=False)

#### Retrieval

    >>> _show_as_string(l[0])
    '{"age": 45, "name": "Peter"}'

    >>> l['1.name']
    'John'

    >>> _show_as_string(l['1.friends'])
    '["Betty", {"name": "Lucy", "since": "1999"}]'

    >>> l['1.friends.0']
    'Betty'

    >>> l['1.friends.1.name']
    'Lucy'

    >>> l['1.friends.0.name']               # Betty is not a dict; see the "silent_fail" option below
    Traceback (most recent call last):
        ...
    KeyError: "Item '0' cannot be traversed deeper."

#### Assignment

    >>> l[1] = 3                            # replace John's dict with a number ->  [{'age': 45, 'name': 'Peter'}, 3]
    >>> _show_as_string(l)
    '[{"age": 45, "name": "Peter"}, 3]'

    >>> l['0.name'] = 'Peter Pan'
    >>> _show_as_string(l)
    '[{"age": 45, "name": "Peter Pan"}, 3]'

    >>> l['3'] = 234
    Traceback (most recent call last):
        ...
    IndexError: list assignment index out of range

    >>> l['+'] = 234
    >>> _show_as_string(l)
    '[{"age": 45, "name": "Peter Pan"}, 3, 234]'

    >>> l['+'] = { 1:[11, 111, 1111] }     # append to the list on the top level
    >>> _show_as_string(l)
    '[{"age": 45, "name": "Peter Pan"}, 3, 234, {"1": [11, 111, 1111]}]'

    >>> l['3.1.+'] = 222
    >>> l['3.1']
    [11, 111, 1111, 222]

#### Deletion

    >>> del l['3.1.2']
    >>> l['3.1']
    [11, 111, 222]

#### `in` operator

    >>> 234 in l
    True

### Dict-based datastructures

    >>> c = Datastructure({
    ...     "item1": {
    ...         "subitem1_1": {
    ...             "name": "John",
    ...             "age": 13,
    ...         },
    ...         "subitem1_2": {
    ...             "name": "Peter",
    ...             "age": 45,
    ...         }
    ...     }
    ... },
    ... silent_fail=False)

#### Accessing values

    >>> _show_as_string(c['item1'])
    '{"subitem1_1": {"age": 13, "name": "John"}, "subitem1_2": {"age": 45, "name": "Peter"}}'

    >>> _show_as_string(c['item1.subitem1_1'])
    '{"age": 13, "name": "John"}'

    >>> c['item1.subitem1_1.name']
    'John'

    # Non-existing elements
    >>> c['item1.subitem1_4']
    Traceback (most recent call last):
        ...
    KeyError: 'subitem1_4'

    >>> c['item1.subitem1_1.name.non-existing']
    Traceback (most recent call last):
        ...
    KeyError: "Item 'name' cannot be traversed deeper."

#### `in` operator

    >>> 'item1' in c
    True
    >>> 'item1.subitem1_1' in c
    True
    >>> 'item1.subitem1_1.name' in c
    True
    >>> 'item1.subitem1_3' in c
    False

#### Assignment

    >>> c['item1.subitem1_1.name'] = 'Hans'
    >>> c['item1.subitem1_1.name']
    'Hans'

    >>> _show_as_string(c['item1.subitem1_1'])
    '{"age": 13, "name": "Hans"}'

    >>> c['item1.subitem1_1.address'] = 'Sofia, Bulgaria'    # assign a new key
    >>> c['item1.subitem1_1.address']
    'Sofia, Bulgaria'

    >>> _show_as_string(c['item1.subitem1_1'])
    '{"address": "Sofia, Bulgaria", "age": 13, "name": "Hans"}'

#### Deletion of items

    >>> c['item1.new_item'] = { 1:11, 2:22 }
    >>> 'item1.new_item' in c
    True

    >>> del c['item1.new_item']
    >>> 'item1.new_item' in c
    False

### Silent mode

    >>> c = Datastructure({
    ...     "item1": {
    ...         "subitem1_1": {
    ...             "name": "John",
    ...             "age": 13,
    ...         },
    ...         "subitem1_2": {
    ...             "name": "Peter",
    ...             "age": 45,
    ...         }
    ...     }
    ... }, silent_fail=True)     # this is the default

    >>> c['item1.subitem1_4']           # will return None

    >>> c['item1.subitem1_1.name']
    'John'

    >>> c['item1.subitem1_1.id']        # will return None

    >>> c['item1.subitem1_4.non-existing'] = '4'  # this is NOOP

    >>> l = Datastructure([
    ...     {
    ...         "name": "Peter",
    ...         "age": 45,
    ...     },
    ...     {
    ...         "name": "John",
    ...         "age": 13,
    ...         "friends": [
    ...             "Betty",
    ...             {
    ...                 "name": "Lucy",
    ...                 "since": '1999',
    ...             },
    ...         ]
    ...     },
    ...     {
    ...         "name": "Luke",
    ...         "age": 23,
    ...     },
    ... ], silent_fail=True)

    >>> l[10]                                               # will return None

    >>> l['0.address']                                      # will return None

    >>> l['0.address'] = 'at home'

    >>> _show_as_string(l['0'])
    '{"address": "at home", "age": 45, "name": "Peter"}'

    >>> l['0.address.street'] = 'Some Street'               # NO OP

    >>> _show_as_string(l['0'])
    '{"address": "at home", "age": 45, "name": "Peter"}'

### Iteration

#### Iteration over key patterns

    >>> _show_as_string(list(l.iterpattern('*.name')))
    '[["0.name", "Peter"], ["1.name", "John"], ["2.name", "Luke"]]'

    >>> _show_as_string(list(l.iterpattern('1.friends.*')))
    '[["1.friends.0", "Betty"], ["1.friends.1", {"name": "Lucy", "since": "1999"}]]'

    # NOTE: the 'null' in the result below is for JSON; "None" in Python
    >>> _show_as_string(list(l.iterpattern('1.friends.*.name')))
    '[["1.friends.0.name", null], ["1.friends.1.name", "Lucy"]]'

    >>> _show_as_string(list(l.iterpattern('*')))
    '[["0", {"address": "at home", "age": 45, "name": "Peter"}], ["1", {"age": 13, "friends": ["Betty", {"name": "Lucy", "since": "1999"}], "name": "John"}], ["2", {"age": 23, "name": "Luke"}]]'

    # NOTE: the 'null' in the result below is for JSON; "None" in Python
    >>> _show_as_string(list(l.iterpattern('*.friends.*.name')))
    '[["1.friends.0.name", null], ["1.friends.1.name", "Lucy"]]'

#### List index iteration

    >>> l = Datastructure([
    ...     {
    ...         "name": "1",
    ...         "sub": [
    ...             {"name": "1.1"},
    ...             {"name": "1.2"},
    ...             {"name": "1.3"},
    ...         ]
    ...     },
    ...     {
    ...         "name": "2",
    ...         "sub": [
    ...             {"name": "2.1"},
    ...             {"name": "2.2"},
    ...             {"name": "2.3"},
    ...         ]
    ...     },
    ... ])

    >>> list(l.iterpattern('*.sub.*.name'))
    [('0.sub.0.name', '1.1'), ('0.sub.1.name', '1.2'), ('0.sub.2.name', '1.3'), ('1.sub.0.name', '2.1'), ('1.sub.1.name', '2.2'), ('1.sub.2.name', '2.3')]

    >>> list(l.iterpattern('*.sub.*'))
    [('0.sub.0', {'name': '1.1'}), ('0.sub.1', {'name': '1.2'}), ('0.sub.2', {'name': '1.3'}), ('1.sub.0', {'name': '2.1'}), ('1.sub.1', {'name': '2.2'}), ('1.sub.2', {'name': '2.3'})]

    # No wildcards
    >>> list(l.iterpattern('1.sub.0.name'))
    [('1.sub.0.name', '2.1')]

#### Dict keys iteration

    >>> l = Datastructure([
    ...     {"name": "1", "counts": {"one": 1, "two": 2, "three": 3}},
    ...     {"name": "2", "counts": {"five": 5, "six": 6, "seven": 7}},
    ... ])

    # should show :
    #   '[["0.counts.one", 1], ["0.counts.three", 3], ["0.counts.two", 2], ["1.counts.five", 5], ["1.counts.seven", 7], ["1.counts.six", 6]]'
    # but iteration over dict keys is not deterministic
    >>> _show_as_string(list(l.iterpattern('*.counts.*')))  # doctest:+ELLIPSIS
    '[[...

    # No wildcards
    >>> list(l.iterpattern('0.counts.two'))
    [('0.counts.two', 2)]

### Custom separator, wildcard and 'last list element' symbols

    >>> l = Datastructure([
    ...     {"name": "1", "counts": {"one": 1, "two": 2, "three": 3}},
    ...     {"name": "2", "counts": {"five": 5, "six": 6, "seven": 7}},
    ... ], separator="/")

    >>> l['0/name']
    '1'
    >>> l['0/counts/two']
    2

    >>> l = Datastructure([
    ...     {
    ...         "name": "1",
    ...         "sub": [
    ...             {"name": "1.1"},
    ...             {"name": "1.2"},
    ...             {"name": "1.3"},
    ...         ]
    ...     },
    ...     {
    ...         "name": "2",
    ...         "sub": [
    ...             {"name": "2.1"},
    ...             {"name": "2.2"},
    ...             {"name": "2.3"},
    ...         ]
    ...     },
    ... ], wildcard="?")

    >>> list(l.iterpattern('?.sub.?.name'))
    [('0.sub.0.name', '1.1'), ('0.sub.1.name', '1.2'), ('0.sub.2.name', '1.3'), ('1.sub.0.name', '2.1'), ('1.sub.1.name', '2.2'), ('1.sub.2.name', '2.3')]

    >>> l = Datastructure({'numbers': [1,2,3,4]}, last_list_element="$")

    >>> l['numbers.$'] = 10
    >>> l['numbers']
    [1, 2, 3, 4, 10]

Classes
-------
Datastructure 
    Usage:
    see module's docstring

    Ancestors (in MRO)
    ------------------
    datastructure.Datastructure
    builtins.object

    Class variables
    ---------------
    CONTAINER_TYPES_SUPPORTED

    DEFAULT_LAST_LIST_ELEMENT

    DEFAULT_SEPARATOR

    DEFAULT_WILDCARD

    Static methods
    --------------
    __init__(self, data, silent_fail=True, wildcard='*', separator='.', last_list_element='+')
        Initialize self.  See help(type(self)) for accurate signature.

    filterpattern(self, pattern, filter_lambda, max_count=None)

    findpattern(self, pattern, value_or_callable)
        :param pattern:
        :type pattern:
        :param value:
        :type value:
        :return:
        :rtype:

    get(self, key, default=None)
        for dict compatibility

    get_container_type(self)

    iteritems(self)
        for dict compatibility

    iterpattern(self, pattern, keyparts=None, data_root=None)
        Iterates the datastructure and yields (key, value) tuples

        :return: (key, value)
        :rtype: tuple

    key_level_up(self, key, levels=1)

    keys(self)

    Instance variables
    ------------------
    CONTAINER_TYPES_SUPPORTED

    silent_fail

    symbol_last_list_element

    symbol_separator

    symbol_wildcard
