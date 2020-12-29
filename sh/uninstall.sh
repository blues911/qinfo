#!/bin/bash
# qinfo uninstall script

if [ ! -d /usr/local/qinfo ]; then
    echo "qinfo is not installed"
    exit 0
fi

if [[ "$(whoami)" != "root" ]]; then
    echo "Error: permission denied (run this script as root)"
    exit 1
fi

echo "Uninstalling..."
rm -f /usr/local/bin/qinfo
rm -rf /usr/local/qinfo
rm -rf ~/.cache/qinfo
echo "OK"