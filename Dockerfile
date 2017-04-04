FROM phusion/baseimage:0.9.20

ENV DEBIAN_FRONTEND noninteractive

RUN apt -qqy update                     \
    && apt -y install                   \
       curl                             \
       firefox                          \
       git                              \
       python-lazy-object-proxy         \
       python-lxml                      \
       python-pip                       \
       python-yaml                      \
       xvfb                             \
    && cd /usr/local/bin/               \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.15.0/geckodriver-v0.15.0-linux64.tar.gz \
       | tar zxf -                      \
    && pip install kibitzr              \
    && apt-get remove -y python-pip curl \
    && apt-get clean
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["kibitzr"]
