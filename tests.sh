#!/bin/bash
# this is a great script
# run a test, then clean up
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -bs 100 -t https -n 10

##########################
### Example tests	##
##########################

### Low latency HTTPS ###
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -b 1000 -t https -n 10

### High latency HTTPS ###
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 120ms -b 1000 -t https -n 10

### Low latency IPFS ###
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 5ms -b 1000 -t ipfs -n 10

### High latency IPFS ###
#python3 ipfs_http_benchmark.py -c 10 -s 50 -cf 10 -d 5ms -ds 120ms -b 1000 -t ipfs -n 10
