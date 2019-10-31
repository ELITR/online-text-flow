# online-text-flow
Online event streaming to improve data and text flows

This project is integrated with [Flask](https://flask.palletsprojects.com), [Click](https://click.palletsprojects.com), [Requests](https://requests.readthedocs.io) and [Setuptools](https://setuptools.readthedocs.io). Start with the installation:

    git clone https://github.com/ELITR/online-text-flow.git
    cd online-text-flow
    git pull
    
    python3 setup.py develop --user    # either
    pip3 install --editable --user .   # or
    
    export PATH=~/.local/bin:$PATH

    cd
    
    online-text-flow
    online-text-flow events -h
    online-text-flow client -h
    online-text-flow server -h
    
    git pull        # no need to reinstall due 
                    # to develop/--editable

## Quick Tips

Process the data locally:

    cat data/en.txt | online-text-flow events
    cat data/en.txt | online-text-flow events --json
    cat data/en.txt | online-text-flow events --text

Run the server locally and post some data:

    online-text-flow server
    
    head -n 80 data/en.txt | online-text-flow events | online-text-flow client en
    head -n 80 data/cs.txt | online-text-flow events | online-text-flow client cs
    
    head -n 80 data/en.txt | online-text-flow-events --json | online-text-flow-client en
    head -n 80 data/cs.txt | online-text-flow-events --json | online-text-flow-client cs
    head -n 80 data/en.txt | online-text-flow events --json | online-text-flow client

View the event stream of the data and post to the endpoint:

- http://127.0.0.1:5000/
- http://127.0.0.1:5000/data
- http://127.0.0.1:5000/post

Run the server remotely and post the data to it from your client:

    @quest.ms.mff.cuni.cz> git pull
    @quest.ms.mff.cuni.cz> online-text-flow server --host 195.113.20.53

    cat data/en.txt | online-text-flow events | online-text-flow client en http://quest.ms.mff.cuni.cz:5000
    cat data/cs.txt | online-text-flow events | online-text-flow client cs http://quest.ms.mff.cuni.cz:5000

View the event stream of the data and post to the endpoint:

- http://quest.ms.mff.cuni.cz:5000
- http://quest.ms.mff.cuni.cz:5000/data
- http://quest.ms.mff.cuni.cz:5000/post

## Further Notes

The code is organized into a Python package of the following structure:

    online-text-flow
    | setup.py
    | MANIFEST.in
    | README.md
    | data
    | | en.txt
    | \ cs.txt
    \ elitr
      | __init__.py
      \ onlinetextflow
        | __init__.py
        | events.py
        | client.py
        | server.py
        | index.html
        \ login.html

The `setup.py` defines a namespace package `elitr` where independent project distributions can be plugged in. Reuse the exact same `elitr/__init__.py` and similar `setup.py` in your plug-in project.

You may try running the modules as executables, or importing them from your code:

    elitr/onlinetextflow/events.py --help
    python3 -m elitr.onlinetextflow.__init__

### online-text-flow / [\_\_init\_\_.py](elitr/onlinetextflow/__init__.py)

    Usage: online-text-flow [OPTIONS] COMMAND [ARGS]...
    
      Entry point for the executables of the online-text-flow project. Replace
      the COMMAND from the list below to learn more details.
    
      Try `online-text-flow COMMAND --help` and `online-text-flow-COMMAND -h`.
    
    Options:
      -h, --help  Show this message and exit.
    
    Commands:
      client  Post data from the standard input as the KIND of events to the...
      events  Turn data from speech recognition into text for machine...
      server  Run the web app to merge, stream, and display online text flow...

### online-text-flow events / [events.py]](elitr/onlinetextflow/events.py)

    Usage: online-text-flow events [OPTIONS]
    
      Turn data from speech recognition into text for machine translation. The
      emitted events are classified sentences rather than text chunks evolving
      in time and disturbing the flow. The complete text is emitted just once.
    
    Options:
      -l, --line  Output the events as lines of artificial timestamps and text,
                  where specific differences in timestamps group the events and
                  classify the text as "complete", "expected", and "incoming".
                  [default: --line]
      -j, --json  Output the events as JSON objects with detailed information
                  about the data, the flow, the text, and other indicators.
      -t, --text  Output the resulting text split into classes by empty lines.
      -h, --help  Show this message and exit.

### online-text-flow client / [client.py]](elitr/onlinetextflow/client.py)

    Usage: online-text-flow client [OPTIONS] [KIND] [URL]
    
      Post data from the standard input as the KIND of events to the URL/post
      endpoint. KIND is empty and URL is http://127.0.0.1:5000 by default. Use
      the --force option to post even if the event's data have not changed.
    
      If an input line contains two integers as artificial timestamps and then
      some text, an event is being built from the consecutive lines while the
      timestamps increase. The specific difference of timestamps on one line
      classifies the text as "complete", "expected", "incoming", or ignored.
    
      If the data on a line is a JSON object, the event being built is posted,
      then the data object is decorated and posted as an event of its own.
    
      Lines that do not fit the logic are ignored. They do not emit the event in
      progress and are printed to the standard error. Use the --verbose option
      to discover the implementation details and the semantics of the events.
    
    Options:
      -f, --force    Force the post even if the event's data have not changed.
                     [default: False]
      -v, --verbose  Print the JSON response from the server and the event's
                     metadata if its data have not changed and were not forced.
                     [default: False]
      -h, --help     Show this message and exit.

### online-text-flow server / [server.py]](elitr/onlinetextflow/server.py)

    Usage: online-text-flow server [OPTIONS]
    
      Run the web app to merge, stream, and display online text flow events.
      Post events at /post and listen to their stream at /data. Browse at /.
    
      http://github.com/ELITR/online-text-flow
    
    Options:
      --host TEXT                 [default: 127.0.0.1]
      --port INTEGER              [default: 5000]
      --debug / --no-debug        [default: False]
      --threaded / --no-threaded  [default: True]
      --ssl_context TEXT          Secure with HTTPS if needed.  [TEXT: adhoc]
      -h, --help                  Show this message and exit.

### [elitr/onlinetextflow/index.html](elitr/onlinetextflow/index.html)

Customize `var flow = {"en": '', "de": '', "cs": ''}` if other kinds or names of event streams are needed. Unnamed events are displayed in all streams. Reload the `/` endpoint to clear the `flow` history of complete text in the browser.

Further subtitling viewport can be probably implemented using the CSS `overflow` and the JQuery `animate` features.

### [elitr/onlinetextflow/login.html](elitr/onlinetextflow/login.html)

Includes the flashing of login and logout messages as provided by Flask. Authentication is simple and credentials are hard-coded just to restrict the viewing of the `/` endpoint. Note that anyone can use or misuse the `/post` and `/data` endpoints once they learn they exist!
