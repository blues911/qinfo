#!/bin/bash
# qinfo install script

if [ -d /usr/local/qinfo ]; then
    echo "qinfo is already installed"
    exit 0
fi

fail=0

if [[ "$(whoami)" != "root" ]]; then
    fail=$((fail + 1))
    echo "Error: permission denied (run this script as root)"
fi

if [[ "$(uname)" != "Linux" ]]; then
    fail=$((fail + 1))
    echo "Error: qinfo works only on Linux"
fi

if [[ "$(which python)" == "" ]]; then
    fail=$((fail + 1))
    echo "Error: python not found"
fi

if [[ "$(which free)" == "" ]]; then
    fail=$((fail + 1))
    echo "Error: free not found"
fi

if [[ "$(which df)" == "" ]]; then
    fail=$((fail + 1))
    echo "Error: df not found"
fi

if [[ "$(which uptime)" == "" ]]; then
    fail=$((fail + 1))
    echo "Error: uptime not found"
fi

if [ ! -d ~/.cache ]; then
    fail=$((fail + 1))
    echo "Error: ~/.cache dir not exists"
fi

if [[ $fail > 0 ]]; then
    exit 1
fi

echo "Installing..."
cp -r ./qinfo /usr/local/qinfo
cp ./sh/qinfo /usr/local/bin/qinfo
echo "Ok"