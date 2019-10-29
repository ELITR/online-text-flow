import click

from .events import main as e
from .client import main as c
from .server import main as s

@click.group()
def main():
    """
    Online Text Flow CLI
    """
    pass

main.add_command(e, 'events')
main.add_command(c, 'client')
main.add_command(s, 'server')

if __name__ == '__main__':
    main()
