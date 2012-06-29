# -*- coding: utf-8 -*-

import os
import sys

def main():
    from maggicc import app

    try:
        debug = sys.argv[1] == 'debug'
    except IndexError:
        debug = False

    app.run(debug=debug)

# main
if __name__ == '__main__':
    sys.exit(main())
