import re
from collections import defaultdict

# All chip names A-Z
CHIPS = [
    'ALU',
    'Add16',
    'And',
    'And16',
    'Bit',
    'CPU',
    'Computer',
    'DMux',
    'DMux4Way',
    'DMux8Way',
    'FullAdder',
    'HalfAdder',
    'Inc16',
    'Memory',
    'Mux',
    'Mux16',
    'Mux4Way16',
    'Mux8Way16',
    'Nand',
    'Not',
    'Not16',
    'Or',
    'Or16',
    'Or8Way',
    'PC',
    'RAM16K',
    'RAM4K',
    'RAM512',
    'RAM64',
    'RAM8',
    'Register',
    'Xor'
]

SINGLELINE_COMMENT_PTN = re.compile(r'\s*//.+')
MULTILINE_COMMENT_PTN = re.compile(r'\s*/\*.*?\*/', re.DOTALL)
MULTISPACES_PTN = re.compile(r'\s+')
CHIPS_PTN = re.compile(
    r'({})\s*\(.+?\)\s*;'
    .format('|'.join(CHIPS))
)


class HDLParser:
    """
    Normalizes HDL file content and counts chips.
    """
    def __init__(self, text: str):
        self.text = text
        self.normalize()

    def sub(self, pattern: re.Pattern, repl: str = ''):
        self.text = pattern.sub(repl, self.text)

    def remove_comments(self):
        # Removes single line and multiple lines comments
        self.sub(SINGLELINE_COMMENT_PTN)
        self.sub(MULTILINE_COMMENT_PTN)

    def remove_breaks(self):
        # Replaces break to a space
        self.text = self.text.replace('\n', ' ')

    def remove_multiple_spaces(self):
        # Replaces multiple spaces with a single space
        self.sub(MULTISPACES_PTN, ' ')

    def normalize(self):
        self.remove_comments()
        self.remove_breaks()
        self.remove_multiple_spaces()

    def count_chips(self) -> dict[str, int]:
        # returns dict[chip_name:chip_count]
        cnt = defaultdict(int)
        for m in CHIPS_PTN.finditer(self.text):
            cnt[m.group(1)] += 1
        return dict(cnt)
