# -*-encoding:utf-8-*-
import subprocess
import os
import time
import re

JAVA_HOME = r'C:\Program Files\Java\jdk1.8.0_91\bin'
LOG_DIR = r'C:\Users\JosephJin\Desktop\ApktoolCacheDir\Log'


def validateStr(ts):
    ts = ts.replace('\\', '/')
    ts = re.sub('/+', '/', ts)
    if os.path.isabs(ts):
        return ts
    else:
        return os.path.abspath(ts)


if __name__ == "__main__":

    logTag = input("please input the filter tag:")
    print('=====================================================================')
    print("tag is:" + logTag)
    print('=====================================================================')
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logName = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + r'.log'

    logTruePath = os.path.join(LOG_DIR, logName)
    if os.path.exists(logTruePath):
        os.remove(logTruePath)

    cmd_clearCache = r'adb logcat -c'
    p = subprocess.Popen(cmd_clearCache, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()

    print(r'clean cache')
    print('=====================================================================')

    cmd = r'adb logcat {0}:D *:S> {1}'.format(logTag,
                                              validateStr(logTruePath))
    # cmd = r'adb logcat {0}:D *:S | tee {1}'.format(logTag, validateStr(logTruePath))
    print('cmd: ' + cmd)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line.decode("gbk"))
    retval = p.wait()

    print('=====================================================================')
    input("press enter to exit")
