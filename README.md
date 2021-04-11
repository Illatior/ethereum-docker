# ethereum-docker

Docker-based environment that could serve as example for building dockerized systems

- - -

## Table of Contents

* [Pre-Requirements](#pre-requirements)
* [Quickstart](#quickstart)
* [Configuration](#configuration)
* [Running](#running)
* [Network topology and configuration](#network-topology-and-configuration)


## Pre-Requirements

+ [Docker](https://www.docker.com/get-docker)

+ [Docker compose](https://docs.docker.com/compose/)

## Quickstart
1. Clone a repo
1. Enter cloned folder
1. Init and update submodules (this step will pull last version of [`go-ethereum`](https://github.com/ethereum/go-ethereum))
```commandline
git submodule init && git submodule update
```
4. Init blockchain with genesis.json
```commandline
sh init.sh
```
That script will build and run `geth` from official [`go-ethereum` repo](https://github.com/ethereum/go-ethereum) in `init` mode.
This needed to initialize ethereum nodes with needed `genesis.json`.

5. Setup bootnode key. 

6. Run docker containers
```commandline
docker-compose up -d
```
7. Enjoy!

## Configuration

Default [docker-compose.yml](./docker-compose.yml) run services isolated, only `15672` port, used to get access to management panel of rabbitmq, are available. 
If you want to get direct access to e.g. database you need to add corresponding port to `port` section of container configuration in [docker-compose.yml](./docker-compose.yml).

### Configuring services

Base configuration of services can be provided by editing base configs that layed in [configs](./configs) directory.
More advanced configuration (e.g. changing base db from postgres to mssql) can be provided only by editing base files. 




## Network topology and configuration

Our default network consists of 2 full client nodes and a 3 mining nodes.
For more information about private ethereum networks, refer to the
[ethereum/go-ethereum documentation on the subject](https://github.com/ethereum/go-ethereum/wiki/Setting-up-private-network-or-local-cluster).

The network is specified in [docker-compose.yaml](./docker-compose.yaml). If you would like to deploy a network with a different topology, this is the place to start.


## Working with nodes from docker host

`ethereum-docker` uses [geth](https://github.com/ethereum/go-ethereum/wiki/geth) under the hood as its
default ethereum node implementation.


### JSON-RPC access with `geth`

By default, we dont expose the [JSON-RPC interface](https://github.com/ethereum/wiki/wiki/JSON-RPC). To
attach to this from your host machine first of all you need to expose rpc port (by default `8545`) and then run (needed geth to be installed on your host machine):

```commandline
geth attach http://localhost:{NODE_RPC_PORT}
```

Here, `NODE_RPC_PORT` refers to the host port specified for your desired node when you brought up
your network.

## Working with a service from its container

For administrative functions especially, you are better off working with a service from its container.
You can do so by running a `bash` process on that container:

```commandline
docker exec -it {SERVICE_CONTAINER} bash
```
or 
```commandline
docker-compose attach {SERVICE_CONTAINER} bash
```

Here, `SERVICE_CONTAINER` specifies the name of the container running the desired service. For our
[sample network](./docker-compose.yaml), you can specify `SERVICE_CONTAINER=redis` to work
with `redis` container and see data in it.

From this shell, run

```commandline
redis-cli
```

for access to the redis and check the data.

## Other

### Utils

There is only one util - [`rmq_password_encoder`](./utils/rmq_password_encoder.py).
This used to encode your password for rmq and then pass to [`configuration`](./configs/rmq/definitions.json).
To run it you need to previously install `python` version `3+`.
After installing you are able to run it with
```commandline
python3 rmq_password_encoder.py {YOUR_PASSWORD_TO_ENCODE}
```

### Hot to optimize python-based service images

Python services provided by this repository can be built via [multi-stage building](https://docs.docker.com/develop/develop-images/multistage-build/)
if you are ready to face manual linking python source codes for used libraries to gcc compiler ([guide](https://stackoverflow.com/questions/39913847/is-there-a-way-to-compile-a-python-application-into-static-binary)).
