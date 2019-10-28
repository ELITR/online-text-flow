import click

from events import main as e
from client import main as c
from server import main as s

@click.group()
def cli():
    """
    Online Text Flow CLI
    """
    pass

cli.add_command(e, 'events')
cli.add_command(c, 'client')
cli.add_command(s, 'server')

if __name__ == '__main__':
    cli()
