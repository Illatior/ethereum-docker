#!/bin/bash

docker-compose -f docker-compose.yml \
               -f docker-compose.init.yml \
               up -d \
               node_1 node_2 miner_1 miner_2 miner_3 bootnode

