FROM python:3.9.1-alpine
COPY . .
RUN python3 ./setup.py install

