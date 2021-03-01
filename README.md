# qinfo

[![Build Status](https://travis-ci.com/smokehill/qinfo.svg?branch=master)](https://travis-ci.com/smokehill/qinfo)
![os](https://img.shields.io/badge/os-linux-green)

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
```

## Install

```
git clone https://github.com/smokehill/qinfo.git
cd qinfo/
pip install .
```