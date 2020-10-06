# Datastructure

Thin wrapper around `dict` or `list` that provides easy access to nested datastructures
that may contain lists, dicts and simple types.

Values can be accessed via a path notation (default: dot-separated).

Supports getting, modifying, appending and removing values from the nested data structure,
iteration over a path pattern and `in` (contains) operation for paths.

Supports either "silent mode", where trying to access non-existing data just returns None,
or can throw KeyError of any of the items along the path does not exist.

Does NOT create a copy of the data structure, which can be very handy for processing existing
complex data (e.g. parsed JSON value).


See [documentation](./docs.md)