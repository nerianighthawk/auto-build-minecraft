FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    default-jre \
    default-jdk
RUN apt install -y openjdk-17-jdk
RUN apt install -y wget

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /minecraft
WORKDIR /minecraft

RUN wget https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.3-44.1.20/forge-1.19.3-44.1.20-installer.jar
RUN java -jar forge-1.19.3-44.1.20-installer.jar --installServer
COPY resources/eula.txt /minecraft/
COPY resources/whitelist.json /minecraft/
COPY resources/ops.json /minecraft/
COPY resources/server.properties /minecraft/
RUN if test -d resources/world; then \
        mkdir /minecraft/world && \
        cp resources/world/* /minecraft/world/; \
    fi

CMD ["/bin/bash", "run.sh"]
