#!/bin/bash

if [ -d /usr/local/qinfo ]; then
    echo "qinfo is already installed"
    exit 0
fi

if [[ "$(uname)" != "Linux" ]]; then
    echo "Error: qinfo works only on Linux"
    exit 1
fi

if [[ "$(whoami)" != "root" ]]; then
    fail=$((fail + 1))
    echo "Error: permission denied (run this script as root)"
    exit 1
fi

if [ ! -d ~/.cache ]; then
    echo "Error: ~/.cache dir not exists"
    exit 1
fi

echo "Installing..."
# install system deps
apt-get install -y procps python
# install qinfo
cp -r ./qinfo /usr/local/qinfo
touch /usr/local/bin/qinfo
chmod +x /usr/local/bin/qinfo
cat << EOF > /usr/local/bin/qinfo
#!/bin/bash

if [ ! -d ~/.cache/qinfo ]; then
    mkdir ~/.cache/qinfo
    chmod 775 ~/.cache/qinfo
fi

$(which python) /usr/local/qinfo/main.py
EOF
echo "Ok"