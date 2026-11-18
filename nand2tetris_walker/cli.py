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


def main(argv = sys.argv):
    if len(argv) < 2:
        logger.error(
            '[ERROR] Provide the path to the nand2tetris project directory.'
        )
        sys.exit(1)

    path_str = argv[1]
    path = Path(path_str)
    if not path.exists():
        logger.error(f'[ERROR] `{path}` does not exists.')
        sys.exit(1)

    if not path.is_dir():
        logger.error(f'[ERROR] `{path}` is not a directory.')
        sys.exit(1)

    tree_roots = []
    if len(argv) > 2:
        if argv[2] == '*':
            # display all trees for wildcard
            tree_roots.extend(CHIPS)
        else:
            tree_roots = argv[2].split(',')
        for root in tree_roots:
            if root not in CHIPS:
                logger.error(
                    f'[ERROR] `{root}` is not a chip name.\n'
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

    for root in tree_roots:
        tree_node = walker.get_tree(root)
        if not tree_node.children:
            # Skip empty tree
            continue
        logger.info('')  # break line
        for pre, fill, node in RenderTree(tree_node):
            logger.info('%s%s' % (pre, node.name))

    sys.exit(0)

if __name__=='__main__':
    main()
