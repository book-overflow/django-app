FROM python:3.8

ARG BE_PORT

RUN apt update -y && \
	apt upgrade -y && \
	pip3 install pipenv && \
	apt -y autoremove && \
    apt -y clean

EXPOSE $BE_PORT

COPY src/django/init.sh .

CMD ["bash", "init.sh"]
