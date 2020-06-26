#!/bin/bash
# this is a great script
# run a test, then clean up
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 500 -d 2 -b 1000 -t ipfs -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 500 -d 2 -b 1000 -t ipfs -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 20 -s 500 -d 2 -b 1000 -t ipfs -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 20 -s 500 -d 2 -b 1000 -t ipfs -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 40 -s 500 -d 2 -b 1000 -t ipfs -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 40 -s 500 -d 2 -b 1000 -t ipfs -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 2000 -d 2 -b 1000 -t ipfs -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 2000 -d 2 -b 1000 -t ipfs -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 20 -s 2000 -d 2 -b 1000 -t ipfs -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 20 -s 2000 -d 2 -b 1000 -t ipfs -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 40 -s 2000 -d 2 -b 1000 -t ipfs -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 40 -s 2000 -d 2 -b 1000 -t ipfs -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 500 -d 2 -b 1000 -t https -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 500 -d 2 -b 1000 -t https -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 2000 -d 2 -b 1000 -t https -ds 2 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 10 -s 2000 -d 2 -b 1000 -t https -ds 20 -n 10
mn -c
python3 ipfs_http_benchmark.py -c 40 -s 2000 -d 2 -b 1000 -t https -ds 2 -n 120
mn -c
python3 ipfs_http_benchmark.py -c 40 -s 2000 -d 2 -b 1000 -t https -ds 2 -n 600
mn -c
python3 ipfs_http_benchmark.py -c 40 -s 2000 -d 2 -b 1000 -t https -ds 2 -n 1200
mn -c
