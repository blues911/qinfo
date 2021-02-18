#!/bin/bash

if [ ! -d /usr/local/qinfo ]; then
    echo "qinfo is not installed"
    exit 0
fi

echo "Uninstalling..."
# uninstall qinfo
sudo rm -f /usr/local/bin/qinfo
sudo rm -rf /usr/local/qinfo
sudo rm -rf ~/.cache/qinfo
echo "Ok"