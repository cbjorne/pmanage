from pmanage.cli import build_parser
from pmanage.db import init_db

def main():
    init_db()
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()