#!/usr/bin/env python3

"""Online Text Flow Server"""

__copyright__ = "2021"
__homepage__  = "http://github.com/ELITR/online-text-flow"
__license__   = "GPL"
__author__    = "Otakar Smrz"
__email__     = "otakar-smrz users.sf.net"


# https://pgjones.gitlab.io/quart/#how-to-guides


from quart import Quart, Blueprint, json, request, session, websocket

import quart
import asyncio
import os
import re
import click

from . import config

try:
    from time import perf_counter_ns as nano
except ImportError:
    from time import perf_counter
    def nano():
        return int(perf_counter() * 1000000000)


end = Blueprint(config.path, __name__, template_folder='.')

url = quart.url_for


DATA = []

OPTS = config.auth


def normal(path):
    path = re.sub('^https?:/+', '', path)
    return 'https://' + path if path else ''

def unwind(path):
    return path.replace('/', ' ').split()

def inline(opts):
    return '/'.join(opts)


async def events():
    queue = asyncio.Queue()
    try:
        DATA.append(queue)
        while True:
            data = await queue.get()
            show = 'event: %s\n' % data['event'] if 'event' in data else ''
            uniq = data['id']
            data = json.dumps(data['data'])
            code = '%sid: %s\ndata: %s\n\n' % (show, uniq, data)
            yield code.encode()
    except:
        DATA.remove(queue)


@end.websocket('/send')
async def send():
    log = quart.current_app.logger
    while True:
        data = json.loads(await websocket.receive())
        secs = nano()
        line = list(DATA)
        for queue in line:
            await queue.put(data)
        log.error("#%s sent to %d clients in %d ns",
                  data['id'], len(line), nano() - secs)


@end.route('/stop', methods=['POST'])
async def stop():
    line = list(DATA)
    for queue in line:
        await queue.put(StopIteration)
    return json.jsonify({'stop': len(line)})


@end.route('/post', methods=['POST'])
async def post():
    data = await request.json
    line = list(DATA)
    for queue in line:
        await queue.put(data)
    return json.jsonify({'post': len(line)})


@end.route('/data')
async def data():
    if OPTS['pass'] == '' or session.get('auth'):
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
    else:
        return quart.redirect(url('.login'))


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
async def menu(path=''):
    data = {'menu': path,
            'hide': request.args.get('hide', ''),
            'show': request.args.get('show', '')}
    for key in data:
        data[key] = unwind(data[key])
        if data[key]:
            session[key] = data[key]
        elif key in session:
            del session[key]
    return quart.redirect(url('.index'))


@end.route('/show/<path:path>')
@end.route('/show/')
async def show(path=''):
    show = unwind(path)
    if show:
        session['show'] = show
    elif 'show' in session:
        del session['show']
    if 'hide' in session:
        del session['hide']
    return quart.redirect(url('.index'))


@end.route('/hide/<path:path>')
@end.route('/hide/')
async def hide(path=''):
    hide = unwind(path)
    if hide:
        session['hide'] = hide
    elif 'hide' in session:
        del session['hide']
    if 'show' in session:
        del session['show']
    return quart.redirect(url('.index'))


@end.route('/view/<path:path>')
@end.route('/view/')
async def view(path=''):
    if path:
        query = request.query_string.decode()
        session['view'] = normal(path) + ('?' + query if query else '')
    elif 'view' in session:
        del session['view']
    return quart.redirect(url('.index'))


@end.route('/')
async def index():
    if OPTS['pass'] == '' or session.get('auth'):
        menu = session.get('menu', OPTS['menu'])
        show = session.get('show', OPTS['show'])
        hide = session.get('hide', OPTS['hide'])
        if hide:
            show = []
            for key in menu:
                if key not in hide:
                    show.append(key)
        return await quart.render_template('index.html', data=url('.data'),
                                           menu=menu, show=show, debug=OPTS['debug'],
                                           view=session.get('view', OPTS['view']))
    else:
        return quart.redirect(url('.login'))


app = Quart(__name__, template_folder='.')

app.secret_key = os.urandom(16)


@app.route('/')
def point():
    return quart.redirect(url(end.name + '.index'))


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('kind', nargs=-1)
@click.option('--path', default=config.path, show_default=True)
@click.option('--port', default=config.port, show_default=True)
@click.option('--host', default=config.host, show_default=True)
@click.option('--user', default=OPTS['user'], show_default=True)
@click.option('--pass', default=OPTS['pass'], show_default=True)
@click.option('--show', default=inline(config.show), show_default=True)
@click.option('--hide', default=inline(config.hide), show_default=True)
@click.option('--view', default=config.view, show_default=True)
@click.option('--menu', default=inline(config.menu), show_default=True)
@click.option('--debug', is_flag=True, default=False)
@click.option('--reload', 'use_reloader', is_flag=True, default=False)
def main(kind, **opts):
    """
    Run the web app to merge, stream, and render online text flow events. Post
    events at /post. Send events thru a websocket at /send instead of posting
    separate requests. Listen to the event stream at /data. Browse at /.

    The KIND of events to browse by default is ['en', 'de', 'cs']. Change this
    for all browsers by mentioning other event kinds on the command line. Set
    the /menu endpoint for a custom menu in the browser, like /menu/en/de/cs,
    and empty to reset.

    The --path PATH specifies the mountpoint of the app within the server. It
    can have the form of 'textflow', 'elitr', 'elitr/monday-seminars', etc. A
    custom setup of the proxy server is necessary to reflect these properly.

    These settings can also be changed in and provided via the config module.

    The --view URL option will embed the linked video or webpage into the app,
    as will do requesting the /view/URL endpoint, like /view/http://youtu.be.
    The scheme is always reset to https, and /view/elitr.eu?s=theaitre works.

    http://github.com/ELITR/online-text-flow
    """
    if kind:
        opts['show'] = inline(kind)
    for key in list(opts):
        if key not in ['host', 'port', 'use_reloader']:
            OPTS[key] = opts[key]
            if key not in ['debug']:
                del opts[key]
    for key in ['menu', 'show', 'hide']:
        OPTS[key] = unwind(OPTS[key])
    OPTS['view'] = normal(OPTS['view'])
    print(' * Path:', OPTS['path'])
    print(' * Opts:', opts)
    print(' * Show:', *OPTS['show'], OPTS['view'])
    print(' * Menu:', *OPTS['menu'])
    app.register_blueprint(end, url_prefix='/' + OPTS['path'])
    if opts['debug']:
        app.run(**opts)
    else:
        from hypercorn.asyncio import serve
        from hypercorn.config import Config
        config = Config()
        config.bind = opts['host'] + ':' + str(opts['port'])
        config.root_path = ''
        asyncio.run(serve(app, config))


if __name__ == '__main__':
    main()
