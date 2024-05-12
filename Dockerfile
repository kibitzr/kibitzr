FROM debian:sid

ENV DEBIAN_FRONTEND noninteractive

RUN apt -qqy update                     \
    && apt -y install                   \
       libffi-dev                       \
       firefox-esr                      \
       git                              \
       jq                               \
       python3                          \
       python3-lazy-object-proxy        \
       python3-lxml                     \
       python3-yaml                     \
       python3-pip                      \
       curl                             \
    && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz | tar zxf -  \
    && mv geckodriver /usr/local/bin/   \
    && apt-get clean                    \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /kibitzr/

RUN cd /kibitzr                         \
    && pip3 install --break-system-packages -e '.[locked]'

WORKDIR /root/

ENV PYTHONUNBUFFERED true

ENTRYPOINT ["kibitzr"]
