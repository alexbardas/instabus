#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='postgresql://hackathon:hackathon@localhost/hackathon', debug='False', repository='db')
