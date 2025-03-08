FROM debian:bullseye-slim
COPY sources.list /etc/apt/sources.list
RUN apt update && apt install -y ttf-mscorefonts-installer libglvnd-dev libglib2.0-0 vim apache2 libapache2-mod-wsgi-py3 python3-pip && pip3 install virtualenv && a2enmod wsgi
COPY ./backend /backend
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY requirements.txt /backend
WORKDIR /backend
RUN virtualenv venv && . venv/bin/activate && pip install -r requirements.txt && chown -R www-data:www-data /backend
