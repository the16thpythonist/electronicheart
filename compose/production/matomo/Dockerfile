FROM matomo:latest

RUN chown -R www-data:www-data /var/www/html
RUN chmod -R 0777 /var/www/html

COPY ./compose/production/matomo/config.ini.php /var/www/html/config/config.ini.php

