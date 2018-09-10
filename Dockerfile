FROM phusion/baseimage:0.11

ENV DEBIAN_FRONTEND noninteractive

RUN apt -qqy update                     \
    && apt -y install                   \
       curl                             \
       firefox                          \
       git                              \
       jq                               \
       python-lazy-object-proxy         \
       python-lxml                      \
       python-yaml                      \
       python-pip                       \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz | tar zxf -  \
    && mv geckodriver /usr/local/bin/   \
    && apt-get remove -y curl           \
    && apt-get clean                    \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /kibitzr/

RUN cd /kibitzr                         \
    && pip install -e .

WORKDIR /root/

ENV PYTHONUNBUFFERED true

ENTRYPOINT ["kibitzr"]
