FROM golang:1.16-alpine as builder

RUN apk update \
    && apk add --no-cache make gcc musl-dev linux-headers git

ADD ./go-ethereum /src/go-ethereum
RUN cd /src/go-ethereum \
    && make clean geth


FROM alpine:latest

COPY --from=builder /src/go-ethereum/build/bin/geth /usr/local/bin

RUN ln -s /usr/local/bin/geth /node

EXPOSE 8545 8546 30301 3030 30303/udp
ENTRYPOINT ["/node"]