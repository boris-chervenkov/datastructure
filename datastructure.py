# -*- coding: utf-8 -*-
"""
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

"""

import warnings


# noinspection PyIncorrectDocstring,PyIncorrectDocstring
class Datastructure(object):
    """
    Usage:
        see module's docstring
    """

    DEFAULT_WILDCARD = '*'
    DEFAULT_SEPARATOR = '.'
    DEFAULT_LAST_LIST_ELEMENT = '+'

    CONTAINER_TYPES_SUPPORTED = (dict, list, tuple)  # the class itself will be added in __init__

    def __init__(self, data, silent_fail=True, wildcard=DEFAULT_WILDCARD, separator=DEFAULT_SEPARATOR, last_list_element=DEFAULT_LAST_LIST_ELEMENT):
        self.CONTAINER_TYPES_SUPPORTED = self.CONTAINER_TYPES_SUPPORTED + (Datastructure,)
        super(Datastructure, self).__init__()
        if not isinstance(data, self.CONTAINER_TYPES_SUPPORTED):
            raise ValueError("Only list, tuple and dict are supported as data.")

        if isinstance(data, Datastructure):
            # Avoid unnecessary nesting
            self.data = data.data
        else:
            self.data = data

        self.silent_fail = silent_fail
        self.symbol_wildcard = wildcard
        self.symbol_separator = separator
        self.symbol_last_list_element = last_list_element

    def __getitem__(self, key):
        try:
            d, k = self._get_object_and_key(key)
            return type(d).__getitem__(d, k)
        except:
            if not self.silent_fail:
                raise
            else:
                return None

    def __setitem__(self, key, value):
        try:
            d, k = self._get_object_and_key(key, allow_last_element_for_lists=True)
            if k == self.symbol_last_list_element:
                return d.append(value)
            else:
                return type(d).__setitem__(d, k, value)
        except:
            if not self.silent_fail:
                raise

    def __contains__(self, key):
        try:
            d, k = self._get_object_and_key(key)
            return type(d).__contains__(d, k)
        except:
            return False

    def __delitem__(self, key):
        try:
            d, k = self._get_object_and_key(key)
            return type(d).__delitem__(d, k)
        except:
            return False


    def __len__(self):
        return len(self.data)


    def __bool__(self):
        return bool(self.data)


    def __repr__(self):
        return self.data.__repr__()

    def __iter__(self):
        return self.data.__iter__()

    def keys(self):
        if isinstance(self.data, dict):
            return self.data.keys()
        else:
            return range(len(self.data))

    def get(self, key, default=None):
        """ for dict compatibility """
        if isinstance(self.data, dict):
            return self.data.get(key, default)
        else:
            if self.silent_fail:
                return default
            else:
                raise AttributeError("get() is not supported when root data is a list")

    def iteritems(self):
        """ for dict compatibility """
        if isinstance(self.data, dict):
            return iter(self.data.items())
        else:
            return []


    def get_container_type(self):
        return type(self.data)


    def iterpattern(self, pattern, keyparts=None, data_root=None):
        """
            Iterates the datastructure and yields (key, value) tuples


            :return: (key, value)
            :rtype: tuple
        """
        if keyparts is not None:
            if not isinstance(keyparts, (list, tuple)):
                raise ValueError("keyparts must be a list/tuple")
        else:
            keyparts = pattern.split(self.symbol_separator)

        data_root = data_root or self.data

        if self.symbol_wildcard in keyparts:
            # pattern iteration
            wildcard_index = keyparts.index(self.symbol_wildcard)
            keys_before = keyparts[:wildcard_index]
            keys_before_as_str_with_separator_suffix = self.symbol_separator.join(keys_before) + (self.symbol_separator if keys_before else '')
            keys_after = keyparts[wildcard_index+1:]

            if keys_before:
                value_containing_wildcard = self._getitem_extended(full_key=None, keyparts=keys_before, data_root=data_root)
            else:
                value_containing_wildcard = self.data

            wildcard_iterator = None
            if isinstance(value_containing_wildcard, dict):
                wildcard_iterator = value_containing_wildcard.items()
            elif isinstance(value_containing_wildcard, (list, tuple)):
                wildcard_iterator = enumerate(value_containing_wildcard)

            if wildcard_iterator is not None:  # => iterating dicts and lists
                # noinspection PyTypeChecker
                for wildcard_key, wildcard_value in wildcard_iterator:
                    if not keys_after:
                        yield keys_before_as_str_with_separator_suffix + str(wildcard_key), wildcard_value
                    else:
                        for k, v in self.iterpattern(pattern=None, keyparts=keys_after, data_root=wildcard_value):
                            yield (
                                "{}{}{}{}".format(
                                    keys_before_as_str_with_separator_suffix,
                                    wildcard_key,
                                    self.symbol_separator,
                                    k
                                ),
                                v
                            )
            else:  # => other type of object - cannot iterate over it
                if self.silent_fail:
                    return None
                else:
                    raise ValueError("Cannot iterate over an object of type '{}'".format(str(type(value_containing_wildcard))))
        else:
            if self.symbol_wildcard in (pattern or keyparts):
                warnings.warn("Wildcard '{0}' is only supported as a separate key segment "
                              "(e.g. 'some.{0}.keys', and not 'some{0}.key'). "
                              "Wildcard will be treated as a normal character".format(self.symbol_wildcard))
            # simply return the item specified by the key
            yield self.symbol_separator.join(keyparts), self._getitem_extended(full_key=None, keyparts=keyparts, data_root=data_root)


    def filterpattern(self, pattern, filter_lambda, max_count=None):
        if not callable(filter_lambda):
            raise ValueError("filter_lambda parameter must be callable")

        filtered_count = 0
        for key, value in self.iterpattern(pattern):
            if filter_lambda(value):
                filtered_count += 1
                yield key, value
                if max_count is not None and filtered_count >= max_count:
                    break


    def findpattern(self, pattern, value_or_callable):
        """

        :param pattern:
        :type pattern:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        filter_lambda = value_or_callable if callable(value_or_callable) else lambda x: x == value_or_callable

        for key, value in self.iterpattern(pattern):
            if filter_lambda(value):
                return key, value

        return None, None

    def key_level_up(self, key, levels=1):
        parts = key.split(self.symbol_separator)
        return self.symbol_separator.join(parts[:-levels])


    def _getitem_extended(self, full_key, allow_last_plus_for_lists=False, keyparts=None, data_root=None):
        try:
            d, k = self._get_object_and_key(full_key,
                                            allow_last_element_for_lists=allow_last_plus_for_lists,
                                            keyparts=keyparts,
                                            data_root=data_root)
            return type(d).__getitem__(d, k)
        except:
            if not self.silent_fail:
                raise
            else:
                return None


    def _get_object_and_key(self, full_key, allow_last_element_for_lists=False, keyparts=None, data_root=None):
        """
        Returns dict instance that can be assigned, and a key to be assigned.
        Will throw KeyError of any of the middle items along the path
        does not represent a dict.

        For example:

            # >>> nd = Datastructure({
            # ...     'item1': {
            # ...         "subitem1_1": {
            # ...             "name": "John",
            # ...             "age": 23,
            # ...         }
            # ...     }
            # ... })

            # >>> nd._get_object_and_key('item1.subitem1_1.name')  # doctest: +NORMALIZE_WHITESPACE
            # ({'age': 23, 'name': 'John'}, u'name')

        """

        if keyparts is not None:
            if not isinstance(keyparts, (list, tuple)):
                raise ValueError("keyparts argument must be a list or a tuple")
            if not all(isinstance(l, (str, int)) for l in keyparts):
                raise ValueError("Only string or int keys are supported")
        else:
            if not isinstance(full_key, (str, int)):
                raise ValueError("Only string or int keys are supported")
            full_key = str(full_key)
            keyparts = full_key.split(self.symbol_separator)

        d = data_root or self.data
        k = None
        for i, k in enumerate(keyparts):
            if isinstance(d, list):
                if k.isdigit():
                    k = int(k)
                elif k == self.symbol_last_list_element and i == len(keyparts)-1 and allow_last_element_for_lists:
                    pass
                else:
                    raise KeyError('Only ints are supported as list indexes, and "+" as a last index for lists.')
            elif isinstance(d, dict):
                if k.isdigit():  # Check if the dict's key is an int
                    k_int = int(k)
                    if k_int in d:
                        k = k_int

            # more iterations are needed => reassign d
            if i < len(keyparts)-1:
                d = type(d).__getitem__(d, k)
                if not isinstance(d, self.CONTAINER_TYPES_SUPPORTED):
                    raise KeyError("Item '{}' cannot be traversed deeper.".format(k))

        return d, k


if __name__ == "__main__":
    import doctest
    doctest.testmod(
        verbose=False,
        report=False,
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.IGNORE_EXCEPTION_DETAIL
    )
