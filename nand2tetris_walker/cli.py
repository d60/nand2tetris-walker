import logging
import sys
from pathlib import Path

from anytree import RenderTree

from .parser import CHIPS
from .walker import HDLWalker

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


def main():
    if len(sys.argv) < 2:
        logger.error(
            '[ERROR] Provide the path to the nand2tetris project directory.'
        )
        sys.exit(1)

    path_str = sys.argv[1]
    path = Path(path_str)
    if not path.exists():
        logger.error(f'[ERROR] `{path}` does not exists.')
        sys.exit(1)

    if not path.is_dir():
        logger.error(f'[ERROR] `{path}` is not a directory.')
        sys.exit(1)

    tree_chip = None
    if len(sys.argv) > 2:
        tree_chip = sys.argv[2]
        if tree_chip not in CHIPS:
            logger.error(
                f'[ERROR] `{tree_chip}` is not a chip name.\n'
                f'Available chip names: {", ".join(CHIPS)}'
            )
            sys.exit(1)

    walker = HDLWalker(path=path)

    try:
        counts = walker.get_nand_counts()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

    logger.info(f'{"Chip": <11} Nand')
    for name in CHIPS:
        if name == 'Nand':
            continue
        count = counts[name]
        if count == 0:
            # ignore count 0 since it has not yet been implemented
            continue
        logger.info(f'{name: <11} {count}')

    if tree_chip:
        logger.info('')
        tree_node = walker.get_tree(tree_chip)
        for pre, fill, node in RenderTree(tree_node):
            logger.info('%s%s' % (pre, node.name))

    sys.exit(0)

if __name__=='__main__':
    main()
