from abc import ABCMeta, abstractmethod


class SimComponent(metaclass=ABCMeta):
    """Component class of Composite pattern describing JASMINE data tree.

    Since JASMINE's data structure is a tree structure, the Composite pattern is applied. Unlike the normal
    Composite pattern, the Composite class is inherited by subclasses.

    Attributes:
        _parent: Parent node.
    """
    def __init__(self):
        self._parent = None

    def get_parent_list(self):
        """ Get parent list.

        Parent object is OnTheSkyCoordinates object. From the position list written in the sky coordinate, calculate
         position list in detector coordinate, and hold it.

        Returns:

        """
        return self._parent.get_list()

    def has_parent(self):
        """Check whether the object has parent or not.

        Returns: if it ha parent return true, otherwise return false.

        """
        return self._parent is not None

    @abstractmethod
    def get_child_size(self):
        pass

    @abstractmethod
    def get_child(self, i: int):
        pass

    @abstractmethod
    def accept(self, v):
        pass
