FROM ubuntu:19.10

WORKDIR /ATTPwn

RUN apt-get update && \
	apt-get -y install python3 git python3-pip

ADD . /ATTPwn

RUN pip3 install -r requirements.txt

#RUN git clone https://github.com/ElevenPaths/ATTPwn

CMD ["python3","app.py"]

