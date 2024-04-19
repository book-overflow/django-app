FROM python:3.8

ARG BE_PORT

RUN apt update -y && \
	apt upgrade -y && \
	apt install libpq-dev -y && \
	apt install gdal-bin -y && \
	pip3 install pipenv && \
	apt -y autoremove && \
	apt -y clean

EXPOSE $BE_PORT

COPY init.sh .

COPY . /app
CMD ["bash", "init.sh"]