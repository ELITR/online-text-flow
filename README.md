# online-text-flow
Online event streaming to improve data and text flows

[Setup](#setup) | [Quick Tips](#quick-tips) | [Further Notes](#further-notes) | [Example](#example) | [Brief Format](#brief-format)

## Setup

This project is integrated with [Quart](https://pgjones.gitlab.io/quart/), [Click](https://click.palletsprojects.com), [Requests](https://requests.readthedocs.io) and [Setuptools](https://setuptools.readthedocs.io). First, clone this repo:

    git clone https://github.com/ELITR/online-text-flow.git
    cd online-text-flow/

Server requires Python>=3.7, the other parts 3.6. Start with creating or activating your virtual environment with the Python3 version you want to use, specified as the `-p` parameter:

    virtualenv p3 -p /usr/bin/python3
    source p3/bin/activate
   
Without virtual environment, you might need `export PATH=~/.local/bin:$PATH`.
    
### Installation

There are two ways to install this tool. The first is for debugging, when you don't mind suboptimal time performance, but you want the changes in the source code to be immediately available for run, without reinstallation. The second way is for performance. Compare their timings by `make check`. Notice that the very first run after installation might be unusually slow, don't count it. Your current system load also has an impact.


#### For debugging
    
    python3 setup.py develop        # either
    pip3 install --editable .       # or
    make develop                    # the first way wrapped in Makefile
    make editable                   # or the other
    
After changing the source codes, or `git pull`, no need to reinstall due to `develop`/`--editable`.
                    
#### For performance

    make
    
After changing the code, `make` again.


## Run

You can now run the following, where `online-text-flow COMMAND` and `online-text-flow-COMMAND` call the same Python code eventually. Without virtual environment, you may need to put `export PATH` into your `~/.bashrc` and possibly introduce some `alias` for convenience.

    online-text-flow
    online-text-flow events -h
    online-text-flow client -h
    online-text-flow server -h
    online-text-flow from_brief -h
    online-text-flow to_brief -h
    
    online-text-flow-events -h
    online-text-flow-client -h
    online-text-flow-server -h    
    online-text-flow-from_brief -h
    online-text-flow-to_brief -h

The [`setup/`](setup/) directory contains the [`nginx`](setup/nginx) config as well as the [`start`](setup/start) and [`stop`](setup/stop) scripts. When activated, **multiple apps** are deployed at **different mountpoints** and available as follows:

- https://quest.ms.mff.cuni.cz/textflow/
- https://quest.ms.mff.cuni.cz/textflow/1/
- https://quest.ms.mff.cuni.cz/textflow/2/
- https://quest.ms.mff.cuni.cz/textflow/3/
- https://quest.ms.mff.cuni.cz/elitr/
- https://quest.ms.mff.cuni.cz/elitr/sg1/
- https://quest.ms.mff.cuni.cz/elitr/monday-seminars/
- https://quest.ms.mff.cuni.cz/elitr/debug/

Use `ws://quest.ms.mff.cuni.cz/textflow`, `ws://quest.ms.mff.cuni.cz/elitr/monday-seminars`, etc. for streaming up the data to the [server](#online-text-flow-server--server__init__py) with the [client](#online-text-flow-client--clientpy) via websockets. Remember to modify both the [nginx](setup/nginx) config and the [setup/](setup/) scripts accordingly if changing or introducing new mountpoints.

The design features of the frontend are described in the [index](#elitronlinetextflowserverindexhtml) and [login](#elitronlinetextflowserverloginhtml) sections.

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

View the event stream of the data and send/post to the endpoint:

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
            onlinetextflow/
                __init__.py
                events.py
                client.py
                server/
                    __init__.py
                    config.py
                    index.html
                    login.html
                    ...
                ...
        setup/
            nginx
            start
            stop
            ...

The [`setup.py`](setup.py) identifies a namespace package `elitr` where independent project distributions can be plugged in. Closely follow the setup and layout of this package in another `elitr` plug-in project.

Next to the `online-text-flow` and `online-text-flow-{events,client,server}` scripts, you may try running the modules as executables, or importing them from your code:

    elitr/onlinetextflow/events.py --help
    python3 -m elitr.onlinetextflow.__init__

The [`server/config.py`](elitr/onlinetextflow/server/config.py) defines the defaults for the [`server/__init__.py`](elitr/onlinetextflow/server/__init__.py), which can be useful if application parameters cannot be provided via a command line.

### online-text-flow / [\_\_init\_\_.py](elitr/onlinetextflow/__init__.py)

    Usage: online-text-flow [OPTIONS] COMMAND [ARGS]...
    
      Entry point for the executables of the online-text-flow project. Replace
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

### online-text-flow events / [events.py](elitr/onlinetextflow/events.py)

    Usage: online-text-flow events [OPTIONS] [LANG]
    
      Turn data from speech recognition into text for machine translation. The
      emitted events are classified sentences rather than text chunks evolving
      in time and disturbing the flow. The complete text is emitted just once.
    
      LANG is the language code passed to MosesSentenceSplitter, 'en' if none.
    
    Options:
      -l, --line    Output the events as lines of artificial timestamps and text,
                    where specific differences in timestamps group the events and
                    classify the text as "complete", "expected", and "incoming".
                    [default: --line]
      -j, --json    Output the events as JSON objects with detailed information
                    about the data, the flow, the text, and other indicators.
      -t, --text    Output the resulting text split into classes by empty lines.
      --timestamps  Output the real events timestamps as the 3rd and 4th space-
                    separated column. The timestamps are approximated from the
                    input segments by length in characters.  [default: False]
      -b, --brief   Input is converted from the "brief" text flow to the original
                    "verbose" protocol with repeated sentences.  [default: False]
      -h, --help    Show this message and exit.

### online-text-flow client / [client.py](elitr/onlinetextflow/client.py)

    Usage: online-text-flow client [OPTIONS] [KIND] [URL]
    
      Emit data as the KIND of events to the URL/send websocket or the URL/post
      endpoint, depending on the scheme of the URL. Consider websockets over
      recurring requests. KIND is '' and URL is ws://127.0.0.1:5000 by default.
    
      If an input line contains two integers as artificial timestamps and then
      some text, an event is being built from the consecutive lines while the
      timestamps increase. The specific difference of timestamps on one line
      classifies the text as "complete", "expected", "incoming", or ignored.
    
      If the data on a line is a JSON object, the event being built is posted,
      then the data object is decorated and posted as an event of its own.
    
      Lines that do not fit the logic are ignored. They do not emit the event in
      progress and are printed to the standard error. Use the --verbose option
      to observe the implementation details and the semantics of the events.
    
    Options:
      -v, --verbose  Print the JSON event and the response code from the server.
                     [default: False]
      -b, --brief    Input is converted from the "brief" text flow to the original
                     "verbose" protocol with repeated sentences.  [default: False]
      -h, --help     Show this message and exit.

### online-text-flow server / [server/\_\_init\_\_.py](elitr/onlinetextflow/server/__init__.py)

    Usage: online-text-flow server [OPTIONS] [KIND]...
    
      Run the web app to merge, stream, and render online text flow events. Post
      events at /post. Send events thru a websocket at /send instead of posting
      separate requests. Listen to the event stream at /data. Browse at /.
    
      The KIND of events to browse by default is ['en', 'de', 'cs']. Change this
      for all browsers by mentioning other event kinds on the command line. Set
      the /menu endpoint for a custom menu in the browser, like /menu/en/de/cs,
      and empty to reset. To control which kinds of events are selected in the
      menu, try /show/cs/en or /hide/de/en in the browser. Configure the server
      defaults via the --menu MENU, --show SHOW, or --hide HIDE options.
    
      The --path PATH specifies the mountpoint of the app within the server. It
      can have the form of 'textflow', 'elitr', 'elitr/monday-seminars', etc. A
      custom setup of the proxy server is necessary to reflect these properly.
    
      These settings can also be changed in and provided via the config module.
    
      The --view URL option will embed the linked video or webpage into the app,
      as will do requesting the /view/URL endpoint, like /view/http://youtu.be.
      The scheme is always reset to https, and /view/elitr.eu?s=theaitre works.
    
      http://github.com/ELITR/online-text-flow
    
    Options:
      --path TEXT     [default: textflow]
      --port INTEGER  [default: 5000]
      --host TEXT     [default: 127.0.0.1]
      --user TEXT     [default: *****]
      --pass TEXT     [default: *****]
      --show TEXT     [default: en/de/cs]
      --hide TEXT     [default: ]
      --view TEXT     [default: ]
      --menu TEXT     [default: en/cs/ar/az/be/bg/bs/da/de/el/es/et/fi/fr/ga/he/hr
                      /hu/hy/is/it/ka/kk/lb/lt/lv/me/mk/mt/nl/no/pl/pt/ro/ru/sk/sl
                      /sq/sr/sv/tr/uk]
    
      --debug
      --reload
      -h, --help      Show this message and exit.

### [elitr/onlinetextflow/server/index.html](elitr/onlinetextflow/server/index.html)

The kind of events to browse by default is ['en', 'de', 'cs']. Change this for all browsers by starting the server with the documented command line parameters. For a custom menu in the browser, set the `/menu` endpoint, like `/menu/en/de/cs`, and empty `/menu` to reset. To control which kinds of events are selected in the menu, click on the menu buttons in the order of the desired display, or set the `/show` and `/hide` endpoints in the browser, like `/show/cs/en` or `/hide/de/en`.

The selected event flows form distinct columns of indexed text snippets on the main screen of the application. There is a menu bar on the right containing further control buttons. The interactivity features of the frontend comprise:
- **Exclude** an event flow from the display by clicking a corresponding button in the menu. **Include** it likewise. The selection is remembered per browser tab and survives a reload of the page. One can thus easily clear the history of the event flows, yet retain the preferred kinds of events in display.
- Event flows are automatically scrolled and aligned at the bottom of the page as new text is being rendered. Click the refresh button in the lower right corner of the screen to scroll to a previous **Review** position and turn the auto scrolling off. Use other user scrolling methods for this, too, and move up or down the page as needed. Click the refresh button again to remember the review position and **Resume** automatic scrolling and event flow alignment.
- **Inspect** any desired text snippet by clicking on it, if running in the `--debug` mode. The text will be copied over into a new tab for easier reference.

In order to embed a custom video or webpage into the app, set the `/view` endpoint in the browser with the URL needed, like
`/view/http://youtu.be` or `/view/elitr.eu?s=theaitre`, and empty to reset. Move or resize the embedded view by dragging its top or bottom margin, respectively. Click the preview button in the side bar to hide and show the video, while its audio can still be listened to.

### [elitr/onlinetextflow/server/login.html](elitr/onlinetextflow/server/login.html)

Includes the flashing of login and logout messages as provided by Quart. Authentication is simple and credentials are set in [server/config.py](elitr/onlinetextflow/server/config.py) only to restrict the viewing of the `/` and `/data` endpoints. Note that the `/send` and `/post` endpoints do not require authorization yet, and `/menu` and `/view` are not secured either!

To log in without the need to fill in the login form, open the `/login?auth=USERNAME:PASSWORD` endpoint.

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

### Timestamps

```
(p3) d@y:~/Plocha/elitr/cruise-control/online-text-flow$ online-text-flow events en --timestamps < data/en.txt  | head -n 20
100 101 130.0 480.0 You...
100 101 130.0 840.0 You should...
100 101 130.0 1200.0 You should...
100 101 130.0 2280.0 You should...
100 101 130.0 10200.0 You should...
100 101 130.0 10560.0 You should...
100 101 130.0 13080.0 You should...
100 101 130.0 14160.0 You should thank.
100 110 130.0 6336.2 You should.
200 201 6336.2 16680.0 Thank there have...
100 110 130.0 5614.3 You should.
200 201 5614.3 17040.0 Thank there have been...
100 110 130.0 5064.3 You should.
200 201 5064.3 17400.0 Thank there have been many...
100 110 130.0 4537.5 You should.
200 201 4537.5 17760.0 Thank there have been many revel...
100 110 130.0 4362.9 You should.
200 201 4362.9 18120.0 Thank there have been many revolution.
100 110 130.0 4207.8 You should.
200 201 4207.8 18480.0 Thank there have been many revolutions...
```

## Brief Format

The distinction between brief and original format is a temporary construction for backward compatibility. After we review or adapt subtitler, we make brief format default and hide it from users.

There are `from_brief` and `to_brief` entry points to convert between them. `client` has parameter `-b` to receive brief format. Communication between `client` and `server` is done with the original format.


The difference is illustrated here:

### Original

```
(p3) d@y:~/Plocha/elitr/cruise-control/online-text-flow$ online-text-flow events en  < data/en.txt  | head -n 20
100 101 You...
100 101 You should...
100 101 You should thank.
100 110 You should.
200 201 Thank there have...
100 110 You should.
200 201 Thank there have been...
100 110 You should.
200 201 Thank there have been many...
100 110 You should.
200 201 Thank there have been many revel...
100 110 You should.
200 201 Thank there have been many revolution.
100 110 You should.
200 201 Thank there have been many revolutions...
100 110 You should.
200 201 Thank there have been many revolutions over the...
100 110 You should.
200 201 Thank there have been many revolutions over the last century.
100 110 You should.
```

### Brief

```
(p3) d@y:~/Plocha/elitr/cruise-control/online-text-flow$ online-text-flow events en -b < data/en.txt  | head -n 20
100 101 You...
100 101 You should...
100 101 You should thank.
100 110 You should.
200 201 Thank there have...
200 201 Thank there have been...
200 201 Thank there have been many...
200 201 Thank there have been many revel...
200 201 Thank there have been many revolution.
200 201 Thank there have been many revolutions...
200 201 Thank there have been many revolutions over the...
200 201 Thank there have been many revolutions over the last century.
200 210 Thank there have been many revolutions over the last century.
300 301 But perhaps...
300 301 But perhaps none...
300 301 But perhaps none as...
200 201 Thank there have been many revolutions over the last century, but perhaps none as sick...
200 201 Thank there have been many revolutions over the last century, but perhaps none as significant...
200 201 Thank there have been many revolutions over the last century, but perhaps none as significant as...
200 210 Thank there have been many revolutions over the last century.
```
