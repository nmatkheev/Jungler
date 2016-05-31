FROM debian
MAINTAINER mephidude <sie.inject@gmail.com>
LABEL Description="Base node image for SampleRabbit app" Vendor="Mephidude" Version="1.0"


RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip
RUN pip3 install requests
