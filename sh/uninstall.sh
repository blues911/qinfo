#!/bin/bash
# qinfo uninstall script

if [[ "$(whoami)" != 'root' ]]; then
    echo "Error: permission denied (run this script as root)"
    exit 1
fi

if [ ! -d /usr/local/qinfo ]; then
    echo "qinfo is not installed"
    exit 0
fi

echo "Uninstalling..."
sudo rm -f /usr/local/bin/qinfo
sudo rm -rf /usr/local/qinfo
echo "OK"