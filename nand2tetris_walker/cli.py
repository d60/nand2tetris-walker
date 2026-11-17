import logging
import sys
from pathlib import Path

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

    try:
        counts = HDLWalker(path=path).get_nand_counts()
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

    for name in CHIPS:
        if name == 'Nand':
            continue
        count = counts[name]
        if count == 0:
            # ignore count 0 since it has not yet been implemented
            continue
        logger.info(f'{name: <11} {count}')

    sys.exit(0)

if __name__=='__main__':
    main()
