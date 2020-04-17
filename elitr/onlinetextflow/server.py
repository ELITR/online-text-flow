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


end = Blueprint('textflow', __name__, template_folder='.')

url = quart.url_for


DATA = []

OPTS = {'user': 'elitr', 'pass': 'elitr'}

MENU = ['en', 'de', 'cs']


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

app.register_blueprint(end, url_prefix='/' + end.name)


@app.route('/')
def point():
    return quart.redirect(url(end.name + '.index'))


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('kind', nargs=-1)
@click.option('--host', default='127.0.0.1', show_default=True)
@click.option('--port', default=5000, show_default=True)
@click.option('--user', default=OPTS['user'], show_default=True)
@click.option('--pass', default=OPTS['pass'], show_default=True)
@click.option('--debug / --no-debug', default=False, show_default=True)
def main(kind, **opts):
    """
    Run the web app to merge, stream, and render online text flow events. Post
    events at /post. Send events thru a websocket at /send instead of posting
    separate requests. Listen to the event stream at /data. Browse at /.

    The KIND of events to browse by default is ['en', 'de', 'cs']. Change this
    on the command line for all browsers. Set the /menu endpoint for a custom
    menu in the browser, like /menu/en/de/cs, and empty to reset.

    http://github.com/ELITR/online-text-flow
    """
    global MENU
    if kind:
        MENU = list(kind)
    for key in ['user', 'pass']:
        OPTS[key] = opts[key]
        del opts[key]
    print(' * Opts:', opts)
    print(' * Menu:', MENU)
    app.run(**opts)


if __name__ == '__main__':
    main()
