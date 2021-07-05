FROM alpine:latest
EXPOSE 139
EXPOSE 445

# Install openssh
RUN apk add --no-cache samba

# Setup S6 Overlay
COPY misc/s6-overlay-amd64.tar.gz /
RUN tar xzf /s6-overlay-amd64.tar.gz -C /

# Setup samba
RUN mkdir -m 777 /srv/samba

ENTRYPOINT ["/init"]