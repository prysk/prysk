""" Cli tool to calculate the md5 checksum for one or multiple files """
import sys
from argparse import (
    ArgumentParser,
    FileType,
)
from hashlib import md5
from typing import (
    Optional,
    Sequence,
)


def _create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("files", metavar="FILE", type=FileType("rb"), nargs="+")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _create_parser()
    args = parser.parse_args(argv)
    for file in args.files:
        hasher = md5()
        hasher.update(file.read())
        print(hasher.hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
