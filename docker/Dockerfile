# syntax=docker/dockerfile:1
FROM ghcr.io/dune-daq/c8-minimal:latest

SHELL ["/bin/bash", "-c"] 

ADD ./workarea /dunedaq/run

COPY ./entrypoint.sh /dunedaq/run

RUN chmod 755 /dunedaq/run/entrypoint.sh
RUN chmod ug+w /dunedaq/run

ENTRYPOINT [ "/dunedaq/run/entrypoint.sh" ]
