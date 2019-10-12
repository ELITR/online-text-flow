# online-text-flow
Online event streaming to improve data and text flows

Run the server locally and post some data:

    ./online-text-flow-server.py
    head -n 80 data/en.txt | ./online-text-flow-client.py en
    head -n 80 data/cs.txt | ./online-text-flow-client.py cs

View the event stream of the data and text flow:

- http://127.0.0.1:5000/
- http://127.0.0.1:5000/flow
- http://127.0.0.1:5000/data
