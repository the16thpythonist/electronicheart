#!/bin/bash

echo "Starting FTP Server"
# https://unix.stackexchange.com/questions/593980/tell-vsftpd-to-log-to-stdout-instead-of-some-file
#vsftpd -vsftpd_log_file=$(tty) &
/etc/init.d/vsftpd start
tail -f /tmp/vsftpd.log &
