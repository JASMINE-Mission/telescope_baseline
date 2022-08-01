FROM python:3.9
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y vim less
RUN apt-get install fonts-liberation graphviz libann0 libcdt5 libcgraph6 libgd3 libgts-0.7-5 libgts-bin libgvc6 libgvpr2 liblab-gamut1 libpathplan4 libxaw7 libxmu6 libxpm4
RUN apt-get install graphviz

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN python -m pip install --upgrade pip setuptools graphviz pylint
COPY ./requirements.txt /tmp
WORKDIR /tmp
RUN python -m pip install -r requirements.txt
