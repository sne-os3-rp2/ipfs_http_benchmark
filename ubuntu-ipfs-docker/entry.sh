#! /bin/bash
ipfs init --profile=badgerds

ipfs key gen publish-key

ipfs daemon --migrate=true --enable-namesys-pubsub --enable-pubsub-experiment &


exec "$@"
