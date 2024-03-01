FROM python:3.8

RUN apt update -y && \
	apt upgrade -y && \
	pip3 install pipenv && \
	apt -y autoremove && \
    apt -y clean

EXPOSE 8000

COPY init.sh .

CMD ["bash", "init.sh"]