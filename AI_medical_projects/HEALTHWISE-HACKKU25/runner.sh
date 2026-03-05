#!/bin/bash

set -e

start() {
    cd fabric-samples/test-network
    ./network.sh up createChannel -ca -c mychannel
    ./network.sh deployCC -ccn patient -ccp ../asset-transfer-basic/chaincode-go -ccl go
    ./organizations/ccp-generate.sh
    cp organizations/peerOrganizations/org1.example.com/connection-org1.json ../../backend_api/fabric_connection/
    echo "COPIED connection-org1.json in fabric_connection"
    cd ../../
    cd backend_api/fabric
    node enrollAdmin.js
    node registerUser.js
}

stop() {
    rm -rf backend_api/fabric_connection/*
    rm -rf backend_api/wallet/*
    ./fabric-samples/test-network/network.sh down
}

# Call the appropriate function based on the argument
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        ;;
esac
