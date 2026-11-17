from pathlib import Path

from .counter import NandCounter
from .parser import HDLParser


class HDLWalker:
    def __init__(self, path: Path):
        # path: Project path (nand2tetris\nand2tetris\projects)
        self.path = path
        self.hdl_files = list(self.path.rglob('*.hdl'))

    def get_chip_counts(self):
        """
        Creates a dict like:
        {
            'Not': {'Nand': 1},
            'And': {'Not': 2, 'Nand': 1},
            ...
        }
        """
        chip_counts = {}
        for f in self.hdl_files:
            parser = HDLParser(f.read_text())
            chip_counts[f.stem] = parser.count_chips()
        return chip_counts

    def get_nand_counts(self):
        """
        Creates a dict like:
        {
            'Not': 1,
            'And': 3,
            ...
        }
        """
        chip_counts = self.get_chip_counts()
        return NandCounter(chip_counts).count()
