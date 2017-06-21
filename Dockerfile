FROM debian
MAINTAINER Zach White <skullydazed@gmail.com>

EXPOSE 5000
RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    python \
    python-pip \
    python-setuptools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN git clone https://github.com/skullydazed/kalerator.git
WORKDIR /kalerator
RUN pip install git+https://github.com/skullydazed/kle2xy.git
RUN pip install -r requirements.txt
WORKDIR /kalerator/src
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD gunicorn -w 8 -b 0.0.0.0:5000 --max-requests 1000 --max-requests-jitter 100 -t 60 kalerator.web.app:app
