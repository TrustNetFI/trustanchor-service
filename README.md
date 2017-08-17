Very initial implementation of a Trust anchor proof-of-concept for Indy.

Uses Django + libindy python wrapper (requires python 3.6 or newer).

Some random startup notes below...

# Get newest version of indy-sdk

    git clone https://github.com/hyperledger/indy-sdk

# Start a test network of nodes

    # Change to the indy-sdk directory
    cd indy-sdk

    # Initial setup (you need to run this only the first time)
    docker network create --subnet 10.0.0.0/8 indy_pool_network
    docker build --build-arg pool_ip=10.0.0.2 -f ci/indy-pool.dockerfile -t indy_pool .

    # Start the nodes
    docker run -d --ip="10.0.0.2" --net=indy_pool_network indy_pool

    # If you need to log, check the contained id with
    docker ps

    # ... and then run this, replacing CONTAINER_ID with the one from the previous command
    docker exec -t -i CONTAINER_ID /bin/bash

    # Get the file and copy to my-test-network.txn
    /home/sovrin/.sovrin/pool_transactions_sandbox

# Register your own Trust Anchor

Source: Steward Scenarios.pdf

    $ sovrin

    > connect test

    > new key with seed 424242424242MyTestTrustAnchor424

    > new key with seed 000000000000000000000000Trustee1

    > send NYM dest=CzvneMT45XwY5eTAVQedLF role=TRUST_ANCHOR verkey=~XgrExLytAX7t2gfJGLXStB

# Start Trust anchor service, generate a new DID to register

    python3.6 manage.py runserver

    # From a different terminal

    ./create_did.py

    # And click the link...
