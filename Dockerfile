FROM python:3.8-buster
ENV PYTHONUNBUFFERED=1

RUN python3 -m venv /root/site

COPY requirements.txt /root/requirements.txt
RUN /root/site/bin/pip3 install --upgrade pip
RUN /root/site/bin/pip3 install -r /root/requirements.txt
