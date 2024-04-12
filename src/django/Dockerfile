FROM python:3.8

ARG BE_PORT


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


RUN apt update -y && \
	apt upgrade -y && \
	apt install libpq-dev -y && \
	apt install gdal-bin -y && \
	pip3 install pipenv && \
	apt -y autoremove && \
	apt -y clean

EXPOSE $BE_PORT

COPY init.sh .

CMD ["bash", "init.sh"]