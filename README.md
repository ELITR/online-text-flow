# online-text-flow
Online event streaming to improve data and text flows

## Quick Tips

Process the data locally:

    cat data/en.txt | ./online-text-flow-events.py
    cat data/en.txt | ./online-text-flow-events.py --json
    cat data/en.txt | ./online-text-flow-events.py --text

Run the server locally and post some data:

    ./online-text-flow-server.py
    
    head -n 80 data/en.txt | ./online-text-flow-events.py | ./online-text-flow-client.py en
    head -n 80 data/cs.txt | ./online-text-flow-events.py | ./online-text-flow-client.py cs
    
    head -n 80 data/en.txt | ./online-text-flow-events.py en --json | ./online-text-flow-client.py
    head -n 80 data/cs.txt | ./online-text-flow-events.py cs --json | ./online-text-flow-client.py
    
    head -n 80 data/en.txt | ./online-text-flow-events.py | ./online-text-flow-client.py
    head -n 80 data/en.txt | ./online-text-flow-events.py --json | ./online-text-flow-client.py

View the event stream of the data and post to the endpoint:

- http://127.0.0.1:5000/
- http://127.0.0.1:5000/data
- http://127.0.0.1:5000/post

## Further Notes

### online-text-flow-events.py

- Without options, produces sentences marked with fake time stamps to conform to the format of ASR, while NMT returns them intact. The difference in fake time stamps distinguishes these types of sentences:
    - complete 100 emitted only once
    - expected 10 emitted with changes until confirmed as complete 
    - incoming 1 emitted with the growing input and changes until ended with \w[.!?]
- --json
- --text
- --help

### online-text-flow-client.py

- Takes the optional URL to which the /post endpoint is appended to post the data. By default, http://127.0.0.1:5000 is used.
- --help

### online-text-flow-server.py

- Takes the optional URL where the server should run. It is http://127.0.0.1:5000 by default.
- --help

### index.html

- The events display template used by the server. By default, listens to the /data endpoint and displays events named "en" and "cs". Unnamed events are displayed in both streams. 
