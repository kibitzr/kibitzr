FROM phusion/baseimage:0.9.20

ENV DEBIAN_FRONTEND noninteractive

RUN apt -qqy update                     \
    && apt -y install                   \
       curl                             \
       firefox=45.0.2+build1-0ubuntu1   \
       git                              \
       jq                               \
       python-lazy-object-proxy         \
       python-lxml                      \
       python-pip                       \
       python-yaml                      \
       xvfb                             \
    && pip install kibitzr              \
    && apt-get remove -y python-pip curl \
    && apt-get clean                    \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONUNBUFFERED true

ENTRYPOINT ["kibitzr"]
