FROM ubuntu
MAINTAINER Harsh Gautam hgautam208@gmail.com
RUN apt -qq update && apt -qq -y upgrade \
 && apt install -qq python3 python3-pip -y && apt clean

WORKDIR /var/project/

RUN python3 -m pip install --upgrade pip setuptools \
 && python3 -m pip --no-cache-dir install tensorflow==2.1.0 keras==2.3.1 pillow

ENTRYPOINT ["/usr/bin/python3"]
