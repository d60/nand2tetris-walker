from pathlib import Path

from anytree import Node

from .counter import NandCounter
from .parser import HDLParser
from .tree import ChipTreeBuilder


class HDLWalker:
    def __init__(self, path: Path):
        # path: Project path (nand2tetris\nand2tetris\projects)
        self.path = path
        self.hdl_files = list(self.path.rglob('*.hdl'))

        # chip_counts cache
        self._chip_counts = None

    def get_chip_counts(self):
        """
        Creates a dict like:
        {
            'Not': {'Nand': 1},
            'And': {'Not': 2, 'Nand': 1},
            ...
        }
        """
        if self._chip_counts:
            return self._chip_counts
        chip_counts = {}
        for f in self.hdl_files:
            parser = HDLParser(f.read_text())
            chip_counts[f.stem] = parser.count_chips()
        self._chip_counts = chip_counts
        return chip_counts

    def get_nand_counts(self) -> dict[str, int]:
        """
        Creates a dict like:
        {
            'Not': 1,
            'And': 3,
            ...
        }
        """
        return NandCounter(self.get_chip_counts()).count()

    def build_tree(self, chip_name: str) -> Node:
        builder = ChipTreeBuilder(self.get_chip_counts())
        return builder.get_node(chip_name)
