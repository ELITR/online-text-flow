"""Online Text Flow CLI"""

__copyright__ = "2019"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


if __name__ == '__main__':

    import click

    from .events import main as e
    from .client import main as c
    #from .server import main as s
    from .to_brief import main as tb
    from .from_brief import main as fb



    @click.group(context_settings={'help_option_names': ['-h', '--help']})
    def main():
        """
        Entry point for the executables of the online-text-flow project. Replace
        the COMMAND from the list below to learn more details.

        Try `online-text-flow COMMAND --help` and `online-text-flow-COMMAND -h`.
        """
        pass


    main.add_command(e, 'events')
    main.add_command(c, 'client')
    #main.add_command(s, 'server')
    main.add_command(tb, 'to_brief')
    main.add_command(fb, 'from_brief')

    main()
