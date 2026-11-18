from copy import deepcopy

from anytree import Node


class ChipTreeBuilder:
    """
    Builds a chip dependency tree like:

    FullAdder
    ├── HalfAdder 2
    │   ├── Xor 1
    │   │   └── Nand 4
    │   └── And 1
    │       ├── Nand 1
    │       └── Not 1
    │           └── Nand 1
    └── Or 1
        ├── Not 2
        │   └── Nand 1
        └── Nand 1
    """

    def __init__(self, chip_counts: dict[str, dict[str, int]]):
        self.chip_counts = chip_counts
        self.nodes: dict[str, Node] = {
            'Nand': Node('Nand')
        }
        self.seen = set()  # for detecting interdependencies

    def get_node(self, chip_name: str, _parent_chip_name: str | None = None):
        # Creates a chip node with children.
        # Returns a copy of the cache if the cache exists.
        # `_parent_chip_name` is used only in error messages
        if chip_name in self.nodes:
            return deepcopy(self.nodes[chip_name])

        if chip_name in self.seen:
            raise RuntimeError(
                f'Interdependencies have been detected: `{chip_name}` and `{_parent_chip_name}`.'
            )
        self.seen.add(chip_name)

        node = Node(chip_name)
        for name, count in self.chip_counts[chip_name].items():
            if chip_name == name:
                raise RuntimeError(f'Self reference found: `{chip_name}`')
            cnode = self.get_node(name)
            cnode.name += f' ({count})'
            cnode.parent = node
        self.nodes[chip_name] = node
        return self.get_node(chip_name)
