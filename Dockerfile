FROM ubuntu:latest
LABEL authors="msaig"

ENTRYPOINT ["top", "-b"]