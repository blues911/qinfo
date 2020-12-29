#!/bin/bash
# qinfo install script

if [ -d /usr/local/qinfo ]; then
    echo "qinfo is already installed"
    exit 0
fi

fail=0

if [[ "$(uname)" != "Linux" ]]; then
    echo "Error: qinfo works only on Linux"
    fail=$((fail + 1))
elif [[ "$(which python)" == "" ]]; then
    echo "Error: python is not installed"
    fail=$((fail + 1))
elif [[ "$(whoami)" != "root" ]]; then
    echo "Error: permission denied (run this script as root)"
    fail=$((fail + 1))
fi

if [[ $fail > 0 ]]; then
    exit 1
fi

echo "Installing..."
cp -r ./qinfo /usr/local/qinfo
mkdir /usr/local/qinfo/cache
chmod 777 /usr/local/qinfo/cache
cp ./sh/qinfo /usr/local/bin/qinfo
echo "OK"