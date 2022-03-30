#!/usr/bin/env python
#

from dotenv import load_dotenv
from hashmaps import app


def main():
    load_dotenv()

    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    main()
