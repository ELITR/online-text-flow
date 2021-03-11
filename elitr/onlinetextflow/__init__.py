"""Online Text Flow CLI"""

__copyright__ = "2019"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"

#import click
import sys

help_msg = """Entry point for the executables of the online-text-flow project. Replace
the COMMAND from the list below to learn more details.

Try `online-text-flow COMMAND --help` and `online-text-flow-COMMAND -h`.

Options:
  -h, --help  Show this message and exit.

Commands:
  client      Emit data as the KIND of events to the URL/send websocket or...
  events      Turn data from speech recognition into text for machine...
  from_brief  Converts from the brief text flow into the original one.
  server      Run the web app to merge, stream, and render online text flow...
  to_brief    Converts into the brief text flow from the original one.
"""


#@click.group(context_settings={'help_option_names': ['-h', '--help']})
def main():
    cmd = sys.argv[1]

    if cmd in ["-h", "--help"]:
        print(help_msg, file=sys.stderr)
        sys.exit(1)
    if cmd == "events":
        from elitr.onlinetextflow.events import main as m
    elif cmd == "client":
        from .client import main as m
    elif cmd == "to_brief":
        from .to_brief import main as m
    elif cmd == "from_brief":
        from .from_brief import main as m
    elif cmd == "server":
        from elitr.otf_server.server import main as m
    sys.argv[0] = " ".join(sys.argv[0:2])
    sys.argv.pop(1)

    m()
    
#from .client import main as c

#main.add_command(e, 'events')
#main.add_command(c, 'client')
#main.add_command(s, 'server')
#main.add_command(tb, 'to_brief')
#main.add_command(fb, 'from_brief')

if __name__ == '__main__':

    main()
