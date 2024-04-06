FROM postgres:16

ARG POSTGRES_PORT

RUN apt update -y && \
	apt upgrade -y && \
	apt install -y postgresql-16-postgis-3 postgresql-16-postgis-3-scripts && \
	apt -y autoremove && \
    apt -y clean

EXPOSE $POSTGRES_PORT

CMD ["postgres"]