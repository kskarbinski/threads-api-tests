def remove_none_from_keys_from_dict(dictionary):
    return {k: v for k, v in dictionary.items() if v is not None}


def vars_recursive(obj, ignore_attributes=None):
    """
    Return an object in a dict format. All obj attributes are converted into key:value pairs.
    Attributes from ignore_attributes are completely ignored and not returned.

    Usage:
        > class A(object):
        >     def __init__(self):
        >         self.a = "a"
        >         self.b = "b"
        >         self.c = "c"

        > a = A()
        > print vars_recursive(obj=a, ignore_attributes=["a", "b"])
        > {'c': 'c'}

    :param any obj: An object
    :param list ignore_attributes: List of attributes to ignore

    :return: dict if passed obj has a __dict__ attribute, otherwise the obj
    """
    if hasattr(obj, "__dict__"):
        data = []

        for key, value in obj.__dict__.items():
            if not callable(value) and not key.startswith("__"):
                if ignore_attributes and key in ignore_attributes:
                    continue
                data.append((key, vars_recursive(obj=value, ignore_attributes=ignore_attributes)))

        return dict(data)
    else:
        return obj
