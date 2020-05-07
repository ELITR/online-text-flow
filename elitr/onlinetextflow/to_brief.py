#!/usr/bin/env python3

import click

try:
    from .textflow_protocol import *
except ImportError:
    from elitr.onlinetextflow.textflow_protocol import *

@click.command(context_settings={'help_option_names': ['-h', '--help']})
def main():
    '''Converts into the brief text-flow.'''
    import sys
    for line in brief_to_original(sys.stdin):
        print(line, flush=True, end="")

if __name__ == "__main__":
    main()

