FROM python:3.6

# Add perl and stdbuf for the mosestokenizer package
COPY . .
RUN python3 ./setup.py install

