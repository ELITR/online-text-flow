FROM python:3.9.1-alpine

# Add perl and stdbuf for the mosestokenizer package
RUN apk add perl coreutils
COPY . .
RUN python3 ./setup.py install

