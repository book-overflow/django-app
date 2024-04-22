FROM python:3.8

ARG BE_PORT

RUN apt update -y && \
	apt upgrade -y && \
	apt install libpq-dev -y && \
	apt install gdal-bin -y && \
	pip3 install pipenv && \
	pip3 install gunicorn==20.1.0 && \
	pip3 install whitenoise==6.4.0 && \
	apt -y autoremove && \
	apt -y clean

EXPOSE $BE_PORT

COPY init.sh .

CMD ["bash", "init.sh"]


