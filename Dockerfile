FROM python:3.7

RUN apt-get update && apt-get install -y \
	xvfb

COPY App/* ./
RUN mkdir ./Trials
COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD python3 communicator.py