"""Online Text Flow"""

__copyright__ = "2021"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


import click
import importlib
import sys


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def name():
    """
    Entry point for the executables of the online-text-flow project. Replace
    the COMMAND from the list below to learn more details.

    Try `online-text-flow COMMAND --help` and `online-text-flow-COMMAND -h`.
    """
    pass


def main():
    """
    Entry point for the executables of the online-text-flow project. Cooler!
    """
    where = ['server', 'events', 'client', 'to_brief', 'from_brief']
    which = sys.argv[1] if len(sys.argv) > 1 else ''
    if which and which in where:
        where = [which]
    for which in where:
        every = importlib.import_module('.' + which, package=__package__)
        name.add_command(every.main, which)
    name()


if __name__ == '__main__':
    main()
