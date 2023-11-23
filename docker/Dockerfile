# syntax=docker/dockerfile:1
FROM ghcr.io/dune-daq/alma9-minimal:latest

SHELL ["/bin/bash", "-c"] 

ADD ./workarea /dunedaq/run

COPY --chmod=755 ./entrypoint.sh /dunedaq/run

RUN chmod ug+w /dunedaq/run

USER 10000:0
ENTRYPOINT [ "/dunedaq/run/entrypoint.sh" ]
