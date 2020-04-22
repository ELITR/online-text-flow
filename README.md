# online-text-flow
Online event streaming to improve data and text flows

[Setup](#setup) | [Quick Tips](#quick-tips) | [Further Notes](#further-notes) | [Example](#example)

## Setup

This project is integrated with [Quart](https://pgjones.gitlab.io/quart/), [Click](https://click.palletsprojects.com), [Requests](https://requests.readthedocs.io) and [Setuptools](https://setuptools.readthedocs.io). Start with the installation:

    git clone https://github.com/ELITR/online-text-flow.git
    cd online-text-flow/
    
    python3 setup.py develop --user     # either
    pip3 install --editable --user .    # or
    
    export PATH=~/.local/bin:$PATH

    git pull        # no need to reinstall due 
                    # to develop/--editable

You can now run the following, where `online-text-flow COMMAND` and `online-text-flow-COMMAND` call the same Python code eventually. You may need to put `export PATH` into your `~/.bashrc` and possibly introduce some `alias` for convenience.

    online-text-flow
    online-text-flow events -h
    online-text-flow client -h
    online-text-flow server -h
    
    online-text-flow-events -h
    online-text-flow-client -h
    online-text-flow-server -h

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

View the event stream of the data and send/post to the endpoint:

- http://127.0.0.1:5000
- http://127.0.0.1:5000/textflow
- http://127.0.0.1:5000/textflow/data
- http://127.0.0.1:5000/textflow/post
- ws://127.0.0.1:5000/textflow/send

Run the server remotely and post the data to it from your client:

    @quest.ms.mff.cuni.cz> git pull
    @quest.ms.mff.cuni.cz> online-text-flow server --host 195.113.20.53

    cat data/en.txt | online-text-flow events | online-text-flow client en ws://quest.ms.mff.cuni.cz:5000/textflow
    cat data/cs.txt | online-text-flow events | online-text-flow client cs ws://quest.ms.mff.cuni.cz:5000/textflow

View the event stream of the data and sedn/post to the endpoint:

- http://quest.ms.mff.cuni.cz:5000
- http://quest.ms.mff.cuni.cz:5000/textflow
- http://quest.ms.mff.cuni.cz:5000/textflow/data
- http://quest.ms.mff.cuni.cz:5000/textflow/post
- ws://quest.ms.mff.cuni.cz:5000/textflow/send

## Further Notes

The code is organized into a Python package of the following structure:

    online-text-flow/
        setup.py
        MANIFEST.in
        README.md
        data/
            en.txt
            cs.txt
        elitr/
            __init__.py
            onlinetextflow/
                __init__.py
                events.py
                client.py
                server.py
                index.html
                login.html

The [`setup.py`](setup.py) defines a namespace package `elitr` where independent project distributions can be plugged in. Reuse the exact same [`elitr/__init__.py`](elitr/__init__.py) and similar [`setup.py`](setup.py) in your plug-in project.

Next to the `online-text-flow` and `online-text-flow-{events,client,server}` scripts, you may try running the modules as executables, or importing them from your code:

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
      client  Emit data from the standard input as the KIND of events to the...
      events  Turn data from speech recognition into text for machine...
      server  Run the web app to merge, stream, and display online text flow...

### online-text-flow events / [events.py](elitr/onlinetextflow/events.py)

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

### online-text-flow client / [client.py](elitr/onlinetextflow/client.py)

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

### online-text-flow server / [server.py](elitr/onlinetextflow/server.py)

    Usage: online-text-flow server [OPTIONS] [KIND]...
    
      Run the web app to merge, stream, and render online text flow events. Post
      events at /post. Send events thru a websocket at /send instead of posting
      separate requests. Listen to the event stream at /data. Browse at /.
    
      The KIND of events to browse by default is ['en', 'de', 'cs']. Change this
      on the command line for all browsers. Set the /menu endpoint for a custom
      menu in the browser, like /menu/en/de/cs, and empty to reset.
    
      http://github.com/ELITR/online-text-flow
    
    Options:
      --host TEXT           [default: 127.0.0.1]
      --port INTEGER        [default: 5000]
      --user TEXT           [default: *****]
      --pass TEXT           [default: *****]
      --debug / --no-debug  [default: False]
      -h, --help            Show this message and exit.

### [elitr/onlinetextflow/index.html](elitr/onlinetextflow/index.html)

The kind of events to browse by default is ['en', 'de', 'cs']. Change this for all browsers by starting the server with the documented command line parameters. For a custom menu in the browser, set the `/menu` endpoint, like `/textflow/menu/en/de/cs`, and empty `/textflow/menu` to reset.

### [elitr/onlinetextflow/login.html](elitr/onlinetextflow/login.html)

Includes the flashing of login and logout messages as provided by Quart. Authentication is simple and credentials are hard-coded just to restrict the viewing of the `/` endpoint. Note that anyone can use or misuse the `/post` and `/data` endpoints once they learn they exist!

To log in without the need to fill in the login form, open the `/textflow/login?auth=username:password`endpoint.

## Example

Let us see how the speech recognition output is transformed into the machine translation input using the text flow [events](#online-text-flow-events--eventspy). First, let us get familiar with the first 30 lines of [`data/en.txt`](data/en.txt#L1):
```
130 480 You... 
130 840 You should... 
130 1200 You should... 
130 2280 You should... 
130 10200 You should... 
130 10560 You should... 
130 13080 You should... 
130 14160 You should thank. 
130 16680 You should. Thank there have... 
130 17040 You should. Thank there have been... 
130 17400 You should. Thank there have been many... 
130 17760 You should. Thank there have been many revel... 
130 18120 You should. Thank there have been many revolution. 
130 18480 You should. Thank there have been many revolutions... 
130 18840 You should. Thank there have been many revolutions over the... 
130 19560 You should. Thank there have been many revolutions over the last century. 
130 20280 You should. Thank there have been many revolutions over the last century. But perhaps... 
130 20640 You should. Thank there have been many revolutions over the last century. But perhaps none... 
130 21000 You should. Thank there have been many revolutions over the last century. But perhaps none as... 
130 21180 You should. Thank there have been many revolutions over the last century, but perhaps none as sick... 
130 21720 You should. Thank there have been many revolutions over the last century, but perhaps none as significant... 
130 22080 You should. Thank there have been many revolutions over the last century, but perhaps none as significant as... 
130 22440 You should. Thank there have been many revolutions over the last century. But perhaps none as significant as the law... 
130 22700 You should. Thank there have been many revolutions over the last century. But perhaps none as significant as the large... 
130 3655 You should. Thank 
3655 23150 there have been many revolutions over the last century, but perhaps none as significant as the longevity red... 
3655 4759 there 
4759 23520 have been many revolutions over the last century, but perhaps none as significant as the longevity revolution. 
4759 23750 have been many revolutions over the last century, but perhaps none as significant as the longevity revolution. 
4759 24600 have been many revolutions over the last century, but perhaps none as significant as the longevity revolution. We... 
```

The first three data lines emit three text flow events, one input line to one output event. The recognized text is still "incoming" and there are no "complete" or "expected" sentences yet:
```json
> head -n 3 data/en.txt | online-text-flow events
100 101 You...
100 101 You should...
100 101 You should...
```
```json
> head -n 3 data/en.txt | online-text-flow events --json | jq -c '.text'`
{"complete":[],"expected":[],"incoming":[[100,101,"You..."]]}
{"complete":[],"expected":[],"incoming":[[100,101,"You should..."]]}
{"complete":[],"expected":[],"incoming":[[100,101,"You should..."]]}
```

Interesting things start to happen with lines [7, 8 ,9](data/en.txt#L7):
```json
> head -n 9 data/en.txt | online-text-flow events --json | tail -n +7 | jq -c '.text'
{"complete":[],"expected":[],"incoming":[[100,101,"You should..."]]}
{"complete":[],"expected":[[100,110,"You should thank."]],"incoming":[]}
{"complete":[],"expected":[[100,110,"You should."]],"incoming":[[200,201,"Thank there have..."]]}
```
The corresponding output in the default `--line` format of events produces multiple lines, with the status of text encoded in the [artificial timestamps](elitr/onlinetextflow/client.py) as discussed above with [events](#online-text-flow-events--eventspy) and [client](#online-text-flow-client--clientpy):
```json
> head -n 9 data/en.txt | online-text-flow events | tail -n +7
100 101 You should...
100 110 You should thank.
100 110 You should.
200 201 Thank there have...
```

Around line [25](data/en.txt#L24), we can observe the first "complete" sentence to be emited, and the "expected" sentence changing back into the "incoming" as the comma `century, but` is reintroduced instead of the period `century. But`:
```json
> head -n 26 data/en.txt | online-text-flow events --json | tail -n 3 | jq -c '.text' 
{"complete":[],"expected":[[100,110,"You should."],[200,210,"Thank there have been many revolutions over the last century."]],"incoming":[[300,301,"But perhaps none as significant as the large..."]]}
{"complete":[[100,200,"You should."]],"expected":[[200,210,"Thank there have been many revolutions over the last century."]],"incoming":[[300,301,"But perhaps none as significant as the large..."]]}
{"complete":[],"expected":[],"incoming":[[200,201,"Thank there have been many revolutions over the last century, but perhaps none as significant as the longevity red..."]]}
```
The corresponding `--line` format of the above events:
```json
> head -n 26 data/en.txt | online-text-flow events --json | tail -n 3 | jq -cr '.text[][]|@tsv' | tr '\t' ' '
100 110 You should.
200 210 Thank there have been many revolutions over the last century.
300 301 But perhaps none as significant as the large...
100 200 You should.
200 210 Thank there have been many revolutions over the last century.
300 301 But perhaps none as significant as the large...
200 201 Thank there have been many revolutions over the last century, but perhaps none as significant as the longevity red...
```

Eventually, with line [30](data/en.txt#L30), we get the following event in `--json`, and can overview the "complete", "expected", and "incoming" text for the whole input using the `--text` option:
```json
> head -n 30 data/en.txt | online-text-flow events --json | tail -n 1 | jq -c '.text' 
{"complete":[],"expected":[[200,210,"Thank there have been many revolutions over the last century, but perhaps none as significant as the longevity revolution."]],"incoming":[[300,301,"We..."]]}
```
```json
> head -n 30 data/en.txt | online-text-flow events --text
You should.

Thank there have been many revolutions over the last century, but perhaps none as significant as the longevity revolution.

We...
```
