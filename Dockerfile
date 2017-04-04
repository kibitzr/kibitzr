FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt -qqy update

RUN apt -y install \
    curl \
    firefox \
    git \
    python-lazy-object-proxy \
    python-lxml \
    python-pip \
    python-yaml \
    xvfb

RUN cd /usr/local/bin/ \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz \
    | tar zxf -

RUN pip install kibitzr

ENTRYPOINT ["kibitzr"]
