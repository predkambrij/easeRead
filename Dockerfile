FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

ARG ARG_UID
ARG ARG_GID

ADD buildscript.sh /

# dunno what's that
ENV NOTVISIBLE "in users profile"

RUN echo "export VISIBLE=now" >> /etc/profile && \
    /buildscript.sh phase1 && \
    /buildscript.sh phase2

USER user

ADD /buildscript2.sh /
RUN /buildscript2.sh phase2

ENTRYPOINT ["anki"]
