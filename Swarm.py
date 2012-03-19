
#!/usr/bin/env python
import Swarm
import argparse
from Swarm import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "TODO")
    parser.add_argument('-V', '--version', action='version', version = '%(prog)s {}'.format(version))
    args = parser.parse_args()
    main()
