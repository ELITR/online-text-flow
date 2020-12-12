#!/usr/bin/env python3

"""Online Text Flow Server"""

__copyright__ = "2020"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


# https://pgjones.gitlab.io/quart/#how-to-guides


from quart import Quart, Blueprint, json, request, session, websocket

import quart
import asyncio
import os
import click

from . import config


end = Blueprint(config.path, __name__, template_folder='.')

url = quart.url_for


DATA = []

OPTS = config.auth

MENU = config.menu


async def events():
    stream = asyncio.Queue()
    try:
        DATA.append(stream)
        while True:
            data = await stream.get()
            show = 'event: %s\n' % data['event'] if 'event' in data else ''
            uniq = data['id']
            data = json.dumps(data['data'])
            code = '%sid: %s\ndata: %s\n\n' % (show, uniq, data)
            yield code.encode()
    except:
        DATA.remove(stream)


@end.websocket('/send')
async def send():
    while True:
        data = json.loads(await websocket.receive())
        for stream in DATA:
            await stream.put(data)


@end.route('/stop', methods=['POST'])
async def stop():
    for stream in DATA:
        await stream.put(StopIteration)
    return json.jsonify({'stop': len(DATA)})


@end.route('/post', methods=['POST'])
async def post():
    data = await request.json
    for stream in DATA:
        await stream.put(data)
    return json.jsonify({'post': len(DATA)})


@end.route('/data')
async def data():
    response = await quart.make_response(
        events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None
    return response


@end.route('/logout')
async def logout():
    session['auth'] = False
    await quart.flash('You have been logged out')
    return quart.redirect(url('.index'))


@end.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        form = await request.form
        auth = form.get('user', '') + ':' + form.get('pass', '')
    else:
        auth = request.args.get('auth', ':')
    if auth == ':':
        return await quart.render_template('login.html', login=url('.login'))
    else:
        session['auth'] = auth == OPTS['user'] + ':' + OPTS['pass']
        if not session['auth']:
            await quart.flash('The credentials are invalid')
        return quart.redirect(url('.index'))


@end.route('/menu/<path:path>')
@end.route('/menu/')
# async
def menu(path=''):
    path = path.replace('/', ' ').split()
    if path:
        session['menu'] = path
    elif 'menu' in session:
        del session['menu']
    return quart.redirect(url('.index'))


@end.route('/')
# async
def index():
    if session.get('auth'):
        return quart.render_template('index.html', data=url('.data'), menu=session.get('menu', MENU))
    else:
        return quart.redirect(url('.login'))


app = Quart(__name__, template_folder='.')

app.secret_key = os.urandom(16)


@app.route('/')
def point():
    return quart.redirect(url(end.name + '.index'))


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('menu', nargs=-1)
@click.option('--path', default=config.path, show_default=True)
@click.option('--port', default=config.port, show_default=True)
@click.option('--host', default=config.host, show_default=True)
@click.option('--user', default=OPTS['user'], show_default=True)
@click.option('--pass', default=OPTS['pass'], show_default=True)
@click.option('--debug', is_flag=True, default=False, show_default=True)
@click.option('--reload', 'use_reloader', is_flag=True, default=False, show_default=True)
def main(menu, **opts):
    """
    Run the web app to merge, stream, and render online text flow events. Post
    events at /post. Send events thru a websocket at /send instead of posting
    separate requests. Listen to the event stream at /data. Browse at /.

    The MENU of events to browse by default is ['en', 'de', 'cs']. Change this
    for all browsers by mentioning other event kinds on the command line. Set
    the /menu endpoint for a custom menu in the browser, like /menu/en/de/cs,
    and empty to reset.

    The --path PATH specifies the mountpoint of the app within the server. It
    can have the form of 'textflow', 'elitr', 'elitr/monday-seminars', etc.
    A custom setup of the proxy server is necessary to reflect these properly.

    These settings can also be changed in and provided via the config module.

    http://github.com/ELITR/online-text-flow
    """
    global MENU
    if menu:
        MENU = list(menu)
    for key in ['user', 'pass']:
        OPTS[key] = opts[key]
        del opts[key]
    print(' * Opts:', opts)
    print(' * Menu:', MENU)
    app.register_blueprint(end, url_prefix='/' + opts['path'])
    app.run(**opts)


if __name__ == '__main__':
    main()
