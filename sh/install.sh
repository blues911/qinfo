#!/bin/bash

if [ -d /usr/local/qinfo ]; then
    echo "qinfo is already installed"
    exit 0
fi

fail=0

if [[ "$(uname)" != "Linux" ]]; then
    fail=$((fail + 1))
    echo "Error: qinfo works only on Linux"
fi

if [ ! -d ~/.cache ]; then
    fail=$((fail + 1))
    echo "Error: ~/.cache dir not exists"
fi

if [[ $fail > 0 ]]; then
    exit 1
fi

echo "Installing..."
# install system deps
sudo apt-get install -y build-essential procps python
# install qinfo
sudo cp -r ./qinfo /usr/local/qinfo
sudo cp ./sh/qinfo /usr/local/bin/qinfo
echo "Ok"