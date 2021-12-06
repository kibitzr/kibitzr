FROM phusion/baseimage:master

ENV DEBIAN_FRONTEND noninteractive

RUN apt -qqy update                     \
    && apt -y install                   \
       libffi-dev                       \
       firefox                          \
       git                              \
       jq                               \
       python3-lazy-object-proxy        \
       python3-lxml                     \
       python3-yaml                     \
       python3-pip                      \
       curl                             \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar zxf -  \
    && mv geckodriver /usr/local/bin/   \
    && apt-get remove -y curl           \
    && apt-get clean                    \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /kibitzr/

RUN cd /kibitzr                         \
    && pip3 install --upgrade pip       \
    && pip3 install -e .

WORKDIR /root/

ENV PYTHONUNBUFFERED true

ENTRYPOINT ["kibitzr"]
