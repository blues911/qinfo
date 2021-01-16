# qinfo

[![Build Status](https://travis-ci.com/smokehill/qinfo.svg?branch=master)](https://travis-ci.com/smokehill/qinfo)

Displays system information based on Linux processes.

Available data:
- Distribution release
- Kernel version
- Uptime
- Load average
- CPU
- RAM
- HDD

Tested only on Debian/Ubuntu OS.

![](example.jpg)

## Dependencies

```
python
procps
lsb-release
```

## Install

```
git clone https://github.com/smokehill/qinfo.git
cd qinfo/
make install
qinfo
```