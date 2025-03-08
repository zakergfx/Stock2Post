FROM debian:buster-slim
RUN apt update && apt install -y apache2 && a2enmod rewrite
COPY ./frontend/ /var/www/html/
COPY htaccess /var/www/html/.htaccess
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
WORKDIR /var/www/html
CMD  ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
