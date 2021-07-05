FROM alpine:latest
EXPOSE 22

# Install openssh
RUN apk add --no-cache openssh

# Setup S6 Overlay
COPY misc/s6-overlay-amd64.tar.gz /
RUN tar xzf /s6-overlay-amd64.tar.gz -C /

# Setup SSH
RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key

ENTRYPOINT ["/init"]