FROM nginx:1.21.3

ARG MEDIA_SERVER_USERNAME
ARG MEDIA_SERVER_PASSWORD

# The folder "/www/media" will be the folder which actually holds the files in the end. As it does not exist by default
# we need to create it. A volume should be mounted to "/www"
RUN mkdir /www && \
    mkdir /www/media && \
    mkdir /www/media/filer_public

# Use our custom nginx configuration
COPY ./compose/production/media/nginx.conf /etc/nginx/nginx.conf

# This will create the password file which manages the HTTP BASIC authentication of the web server. These same env
# variables will then also be used by the django container to send them with each request.
RUN apt-get update
RUN apt-get install -y apache2-utils
RUN htpasswd -c -b /www/django.passwd "$MEDIA_SERVER_USERNAME" "$MEDIA_SERVER_PASSWORD"

# == INSTALLING FTP SERVER
RUN apt-get install -y whois && \
    apt-get install -y vsftpd

# -- USE CUSTOM CONFIGURATION
COPY ./compose/production/media/vsftpd.conf /etc/vsftpd.conf
COPY ./compose/production/media/40-start-ftp-server.sh /docker-entrypoint.d/40-start-ftp-server.sh

# -- CREATING A NEW USER FOR THE FTP SERVICE
# https://askubuntu.com/questions/94060/run-adduser-non-interactively
USER 0
RUN whoami && \
    mkpasswd -m sha-512 $MEDIA_SERVER_PASSWORD > /tmp/passwd && \
    export PASSWORD_HASH=$(cat /tmp/passwd) && \
    useradd -U --home-dir /www --password $PASSWORD_HASH $MEDIA_SERVER_USERNAME && \
    cut -d: -f1 /etc/passwd && \
    chmod 0555 /www && \
    chmod -R 0777 /www/media && \
    chown -R "$MEDIA_SERVER_USERNAME:$MEDIA_SERVER_USERNAME" /www/media

# -- CREATING THE VSFTPD USERLIST
RUN echo $MEDIA_SERVER_USERNAME > /etc/vsftpd.userlist

RUN touch /tmp/vsftpd.log
