FROM ubuntu:trusty

# Setup the ftp server
RUN apt-get update \
    && apt-get install -y --no-install-recommends zip unzip vsftpd cron systemd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setup FTP folders
RUN mkdir -p /var/run/vsftpd/empty \
    && mkdir -p /etc/vsftpd \
    && mkdir -p /var/ftp \
    && mv /etc/vsftpd.conf /etc/vsftpd.orig

# Create the FTP service
COPY init /

# Setup the user
RUN useradd -rm -d /home/user -s /bin/bash -u 3232 user \
    && echo 'user:password' | chpasswd \
    && chmod +x /init

# Setup shared volume
# VOLUME ["/var/ftp"]

EXPOSE 20-21
EXPOSE 65500-65515

# When container is run, run the script
ENTRYPOINT ["/init"]
