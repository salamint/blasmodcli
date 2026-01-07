#!/bin/env python3
import sys

from blasmodcli.application import Application


def main() -> int:
    app = Application()
    return app.run()


if __name__ == '__main__':
    sys.exit(main())
