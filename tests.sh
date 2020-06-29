#!/bin/bash
# this is a great script
# run a test, then clean up
mn -c
# Default low latency network
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -b 1000 -t ipfs -n 10
#mn -c

# 10* to demonstrate effect of peering
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 120ms -b 1000 -t ipfs -n 10
mn -c
# Fast root, slow swarm
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 80ms -ds 10ms -b 1000 -t ipfs -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 120ms -ds 10ms -b 1000 -t ipfs -n 10
#mn -c
#
## Equals pequals
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 10ms -ds 10ms -b 1000 -t ipfs -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 80ms -ds 80ms -b 1000 -t ipfs -n 10
#mn -c
#
## More files of smaller size
#python3 ipfs_http_benchmark.py -c 10 -s 5 -cf 100 -d 5ms -ds 5ms -b 1000 -t ipfs -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 10 -s 1 -cf 500 -d 5ms -ds 5ms -b 1000 -t ipfs -n 10
#mn -c
#
## Slow everyone
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 300 -ds 300 -b 1000 -t ipfs -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 300 -ds 300 -b 1000 -t ipfs -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 300 -ds 300 -b 1000 -t ipfs -n 10
#mn -c


#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 2 -b 1000 -t ipfs -ds 20 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 50 -cf 10 -d 2 -b 1000 -t ipfs -ds 2 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 50 -cf 10 -d 2 -b 1000 -t ipfs -ds 20 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 40 -s 50 -cf 10 -d 2 -b 1000 -t ipfs -ds 2 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 40 -s 50 -cf 10 -d 2 -b 1000 -t ipfs -ds 20 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 10 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 2 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 10 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 20 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 2 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 20 -n 10
#mn -c
## Effect of high latency root server vs fast network
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 200 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 10 -b 1000 -t ipfs -ds 200 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 20 -b 1000 -t ipfs -ds 200 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 150 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 10 -b 1000 -t ipfs -ds 150 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 20 -b 1000 -t ipfs -ds 150 -n 10
#mn -c
## Effect of low latency root server vs fast network
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 10 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 10 -b 1000 -t ipfs -ds 10 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 20 -b 1000 -t ipfs -ds 10 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 2 -b 1000 -t ipfs -ds 20 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 10 -b 1000 -t ipfs -ds 20 -n 10
#mn -c
#python3 ipfs_http_benchmark.py -c 20 -s 200 -cf 10 -d 20 -b 1000 -t ipfs -ds 20 -n 10
#mn -c

# TODO: effect of low latency root server fs slow network

# TODO: effect of long naptime on file propagation

# TODO: effect of global low bandwidth on overall download times
