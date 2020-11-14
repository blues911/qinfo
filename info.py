import os
import re
import time
import subprocess


def __bytes_to(bytes, to, b_size = 1024):
    a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    r = float(bytes)

    for i in range(a[to]):
        r = r / b_size

    return r

def cpu():
    # https://supportcenter.checkpoint.com/supportcenter/portal?eventSubmit_doGoviewsolutiondetails=&solutionid=sk65143
    # https://rosettacode.org/wiki/Linux_CPU_utilization
    resp = []

    info = subprocess.check_output('cat /proc/stat | grep -i cpu[0-9+]', shell=True)
    old_info = []
    for line in info.splitlines():
        line = ' '.join(re.sub(r'cpu[0-9+]', '', line).split()).split(' ')
        line = [float(l) for l in line]

        old_info.append([line[3], sum(line)])

    time.sleep(0.5)

    info = subprocess.check_output('cat /proc/stat | grep -i cpu[0-9+]', shell=True)
    i = 0
    for line in info.splitlines():
        line = ' '.join(re.sub(r'cpu[0-9+]', '', line).split()).split(' ')
        line = [float(l) for l in line]

        idle, total = line[3], sum(line)
        idle_delta, total_delta = idle - old_info[i][0], total - old_info[i][1]
        try:
            utilisation = 100.0 * (1.0 - idle_delta / total_delta)
        except:
            # Traceback [ZeroDivisionError: float division by zero].
            # It happens if try to change screen size rapidly.
            utilisation = 0.0

        r = {}
        r['name'] = 'core' + str(i + 1)
        r['used'] = "%.0f" % utilisation

        resp.append(r)
        i = i + 1

    return resp

def mem():
    resp = {}

    # expected: [total, used, free, shared, buff/cache, available]
    info = subprocess.check_output('free | grep -i mem', shell=True)
    info = ' '.join(re.sub('Mem:', '', info).split()).split(' ')

    size = __bytes_to(int(info[0]) * 1024, 'g')
    used = __bytes_to(int(info[1]) * 1024, 'g')

    resp['size'] = "%.1f" % size if int(size) > 0 else str(0)
    resp['used'] = "%.1f" % used if int(used) > 0 else str(0)

    return resp

def swp():
    resp = {}

    # expected: [total, used, free, shared, buff/cache, available]
    info = subprocess.check_output('free | grep -i swap', shell=True)
    info = ' '.join(re.sub('Swap:', '', info).split()).split(' ')

    size = __bytes_to(int(info[0]) * 1024, 'g')
    used = __bytes_to(int(info[1]) * 1024, 'g')

    resp['size'] = "%.1f" % size if int(size) > 0 else str(0)
    resp['used'] = "%.1f" % used if int(used) > 0 else str(0)

    return resp

def hdd():
    resp = []

    # expected: [filesystem, size, used, available, use%, mounted on]
    info = subprocess.check_output('df | grep \'sda\'', shell=True)
    for line in info.splitlines():
        line = ' '.join(line.split()).split(' ')

        r = {}
    
        size = __bytes_to(int(line[1]) * 1024, 'g')
        used = __bytes_to(int(line[2]) * 1024, 'g')

        r['name'] = line[5]
        r['size'] = "%.0f" % size if int(size) > 0 else str(0)
        r['used'] = "%.0f" % used if int(used) > 0 else str(0)

        resp.append(r)

    return resp

def upt():
    info = subprocess.check_output('uptime', shell=True)
    info = ' '.join(re.sub(r'[0-9+] user,', '', info).split())

    return info

def lsb():
    file_path = '.lsb_release'

    if os.path.isfile(file_path) == False:
        # release
        info1 = subprocess.check_output('lsb_release -i -r', shell=True)
        info1 = [''.join(line.split(':')[1].split()) for line in info1.splitlines()]
        info1 = ' '.join(info1)

        # architecture
        info2 = subprocess.check_output('uname -m', shell=True)
        info2 = info2.rstrip()

        # kernel
        info3 = subprocess.check_output('uname -s -r', shell=True)
        info3 = info3.rstrip()

        info_all = info1 + ' ' + info2 + ', ' + info3

        f = open(file_path, 'w')
        f.write(info_all)
        f.close()

        return info_all

    else:
        f = open(file_path, 'r')
        return f.readline()