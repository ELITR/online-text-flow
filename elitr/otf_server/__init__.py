"""Online Text Flow Server"""


import click

from .server import main as s


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def main():
    """
    Entry point for the executables of the online-text-flow project. Replace
    the COMMAND from the list below to learn more details.

    Try `online-text-flow COMMAND --help` and `online-text-flow-COMMAND -h`.
    """
    pass

main.add_command(s, 'server')

if __name__ == '__main__':
    main()
