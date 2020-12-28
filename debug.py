import info


def debug(value=None):
    exec_func = ('cpu','mem','swp','hdd','upt','lsb')

    if value is None:
        print(info.cpu()) # [{'used': '4', 'name': 'core1'}, {'used': '6', 'name': 'core2'}]
        print(info.mem()) # {'size_f': 'G', 'used': '2.9', 'used_f': 'G', 'size': '11.7'}
        print(info.swp()) # {'size_f': 'G', 'used': '0.0', 'used_f': 'K', 'size': '22.9'}
        print(info.hdd()) # [{'size_f': 'G', 'used': '18', 'name': '/', 'used_f': 'G', 'size': '182'}]
        print(info.upt()) # 16:06:35 up 6:00, load average: 0.50, 0.46, 0.53
        print(info.lsb()) # Ubuntu 18.04 x86_64, Linux 5.3.0-59-generic

    else:
        values = value.split(',') # cpu,mem...
        values = [v.strip() for v in values]

        for v in values:
            if v in exec_func:
                print(eval('info.' + v + '()'))


if __name__ == "__main__":
    debug()