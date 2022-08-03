from abc import ABC
from telescope_baseline.tools.pipeline.simcomponent import SimComponent


class SimNode(SimComponent, ABC):
    """Composite class of Composite pattern describing JASMINE data tree.

    Attributes:
        _child: A list of child nodes.
    """

    def __init__(self):
        super().__init__()
        self._child = []

    def get_child_size(self):
        return len(self._child)

    def get_child(self, i: int):
        return self._child[i]

    def add_child(self, c: SimComponent):
        """Add method.

        Args:
            c: Child node to add.

        Returns:void

        """
        self._child.append(c)
        c._parent = self
