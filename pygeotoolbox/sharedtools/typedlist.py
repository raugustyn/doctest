#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE


class TypedList(list):
    """List class for store specific value types."""

    def __init__(self, itemType=int, seq=()):
        """Initialize typed list instance.

        :param type: Type of items allowed.
        :param seq: Initial items sequence.

        >>> TypedList(int, [5, 6])
        [5, 6]
        >>> TypedList(basestring, ["5", "6"])
        ["5", "6"]

        """
        self.itemType = itemType
        for item in seq:
            self.__validateItem(item)
        list.__init__(self, seq)


    def __validateItem(self, item):
        """Valudates value prior it's placing into list. If not, raise TypeError.

        :param item: Item to be validated.
        """
        if hasattr(item, "__class__"):
            cls = item.__class__
        else:
            cls = item
        if not issubclass(cls, self.itemType):
            raise TypeError('%r value is not allowed in %r list.' % (item, self.itemType.__name__))


    # Original methods with type validation
    def append(self, p_object):
        """Validate and append p_object."""
        self.__validateItem(p_object)
        list.append(self, p_object)


    def insert(self, index, p_object):
        """Validate and insert p_object."""
        self.__validateItem(p_object)
        list.insert(self, index, p_object)


    def extend(self, iterable):
        """Validate each item in iterable and extends list by it."""
        for item in iterable:
            self.__validateItem(item)
        list.extend(self, iterable)


    def asDict(self, deep=True):
        result = []
        for item in self.__iter__():
            if hasattr(item, "asDict"):
                result.append(item.asDict(deep))
        return result



# @NO-PRODUCTION CODE
if __name__ == "__main__":
    print TypedList.__init__.__doc__
    intList = TypedList(int, [5, 6]) # OK
    intList.append('44') # raise error
    print intList