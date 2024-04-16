#!/bin/zsh
scp -r iot@172.16.69.1:/home/iot/dev/edge ./edge
scp -r iot@172.16.69.1:/home/iot/dev/node1 ./node_actuator
scp -r iot@172.16.69.90:/home/iot/dev/node2 ./node_sensor
