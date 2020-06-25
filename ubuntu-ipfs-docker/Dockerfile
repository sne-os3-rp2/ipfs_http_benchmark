FROM ubuntu:trusty

WORKDIR /tmp/ipfs
RUN mkdir go-ipfs
COPY ./go-ipfs ./go-ipfs
RUN cd ./go-ipfs && ./install.sh

RUN apt-get update
RUN apt-get install --assume-yes wget
RUN apt-get install --assume-yes nginx

# Copy Nginx certificates after installation
COPY ./self_cert/ /etc/ssl/
COPY default /etc/nginx/sites-enabled/default
#TODO: generate/edit nginx config

# Expose ports
# Swarm TCP; should be exposed to the public
EXPOSE 4001
# Swarm UDP; should be exposed to the public
EXPOSE 4001/udp
# Daemon API; must not be exposed publicly but to client services under you control
EXPOSE 5001
# Web Gateway; can be exposed publicly with a proxy, e.g. as https://ipfs.example.org
EXPOSE 8080
# Swarm Websockets; must be exposed publicly when the node is listening using the websocket transport (/ipX/.../tcp/8081/ws).
EXPOSE 8081

COPY ./entry.sh /entry.sh

ENTRYPOINT ["/entry.sh"]

CMD ["/bin/bash"]

