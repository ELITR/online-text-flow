# online-text-flow
Online event streaming to improve data and text flows

Process the data locally:

    cat data/en.txt | ./online-text-flow-events.py en | jq '.data.text'
    cat data/cs.txt | ./online-text-flow-events.py cs | jq '.data.text'

Run the server locally and post some data:

    ./online-text-flow-server.py
    head -n 80 data/en.txt | ./online-text-flow-events.py en | ./online-text-flow-client.py
    head -n 80 data/cs.txt | ./online-text-flow-events.py cs | ./online-text-flow-client.py

View the event stream of the data and post to the endpoint:

- http://127.0.0.1:5000/
- http://127.0.0.1:5000/data
- http://127.0.0.1:5000/post
