# qinfo

Displays simple system information (in real time) based on general Linux commands.

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