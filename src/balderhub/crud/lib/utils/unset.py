

# pylint: disable-next=invalid-name
class _UNSET_TYPE:
    """
    Type for UNSET values. This object is used within :class:`FieldFillerCallback` to define that a field should
    explicitly be unset.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_UNSET_TYPE, cls).__new__(cls)
        return cls._instance

    def __repr__(self):
        return "UNSET"

    def __eq__(self, other):
        return isinstance(other, _UNSET_TYPE)

    def __hash__(self):
        return hash(type(self))


UNSET = _UNSET_TYPE()
