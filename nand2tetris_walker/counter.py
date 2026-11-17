from .parser import CHIPS


class NandCounter:
    def __init__(self, chip_counts: dict[str, dict[str, int]]):
        self.chip_counts = chip_counts
        self.nand_count: dict[str, int] = {'Nand': 1}
        self.seen = set()  # for detecting interdependencies

    def count(self) -> dict[str, int]:
        # returns dict[chipName: nandCount]
        for name in CHIPS:
            self.get_nand_count(name)
        return self.nand_count

    def get_nand_count(self, chip_name: str, _parent_chip_name: str | None = None) -> int:
        # calclates nand count recursively
        # `_parent_chip_name` is used only in error messages
        if chip_name in self.nand_count:
            return self.nand_count[chip_name]

        if chip_name in self.seen:
            raise RuntimeError(f'Interdependencies have been detected: `{chip_name}` and `{_parent_chip_name}`.')
        self.seen.add(chip_name)

        cnt = 0
        for name, count in self.chip_counts[chip_name].items():
            if chip_name == name:
                raise RuntimeError(f'Self reference found: `{chip_name}`')
            cnt += self.get_nand_count(name, chip_name) * count
        self.nand_count[chip_name] = cnt
        return cnt
