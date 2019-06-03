#-*-encoding:utf-8-*-
import subprocess
import os
import sys
import traceback
import xml.etree.ElementTree as ET

#apktool的存放路径，也是后面反编译的默认工作目录
APKTOOL_WORK_DIR = r'D:\Program_Files\apktool'
# apktool的名称，需和本地的一致
APKTOOL_v1_5_3_NAME = r'apktool-1.5.3.jar'
APKTOOL_v2_0_1_NAME = r'apktool_2.0.1.jar'
APKTOOL_v2_0_3_NAME = r'apktool_2.0.3.jar'
APKTOOL_v2_1_0_NAME = r'apktool_2.1.0.jar'
APKTOOL_v2_2_1_NAME = r'apktool_2.2.1.jar'
APKTOOL_v2_3_3_NAME = r'apktool_2.3.3.jar'

#apktool版本，需和上面的名称一致
APKTOOL_VERSION_1_5_3 = '1.5.3'
APKTOOL_VERSION_2_0_1 = '2.0.1'
APKTOOL_VERSION_2_0_3 = '2.0.3'
APKTOOL_VERSION_2_1_0 = '2.1.0'
APKTOOL_VERSION_2_2_1 = '2.2.1'
APKTOOL_VERSION_2_3_3 = '2.3.3'

#缓存路径
APKTOOL_CACHE = r"E:\pythondcache"

#java环境变量
JAVA_HOME = r'C:\Program Files\Java\jdk1.8.0_91\bin'

androidNS = 'http://schemas.android.com/apk/res/android'
androidN = 'android'

def executeApktool(apktool_version,dest_dir):
    #切换工作目录
    os.chdir(APKTOOL_WORK_DIR)
    for dir in dest_dir:
        term_dir = os.path.join(os.path.abspath(os.curdir),dir)
        print("dest_dir:"+term_dir)
        #if not os.path.exists(term_dir):
            #os.makedirs(term_dir)
        print('=====================================================================')
    #组装命令
    cmd_command = []
    if 'all' in apktool_version:
            cmd_command = [
                r'java -jar {0} d -f "{1}"  {2}'.format(APKTOOL_v1_5_3_NAME,apk_name,dest_dir[APKTOOL_VERSION_1_5_3]),
                r'java -jar {0} d "{1}" -f -o  {2}'.format(APKTOOL_v2_0_1_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_0_1]),
                r'java -jar {0} d "{1}" -f -o {2}'.format(APKTOOL_v2_0_3_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_0_3]),
                r'java -jar {0} d "{1}" -f -o  {2}'.format(APKTOOL_v2_1_0_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_1_0]),
                r'java -jar {0} d "{1}" -f -o  {2}'.format(APKTOOL_v2_2_1_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_2_1]),
                r'java -jar {0} d "{1}" -f -o  {2}'.format(APKTOOL_v2_3_3_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_3_3])
            ]
    else:
        if (APKTOOL_VERSION_1_5_3 in apktool_version):
            cmd_command.append(r'java -jar {0} d -f "{1}" {2}'.format(APKTOOL_v1_5_3_NAME,apk_name,dest_dir[APKTOOL_VERSION_1_5_3]))
        if (APKTOOL_VERSION_2_0_1 in apktool_version):
            cmd_command.append(r'java -jar {0} d "{1}" -f -o {2}'.format(APKTOOL_v2_0_1_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_0_1]))
        if (APKTOOL_VERSION_2_0_3 in apktool_version):
            cmd_command.append(r'java -jar {0} d "{1}" -f -o {2}'.format(APKTOOL_v2_0_3_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_0_3]))
        if (APKTOOL_VERSION_2_1_0 in apktool_version):
            cmd_command.append(r'java -jar {0} d "{1}" -f -o {2}'.format(APKTOOL_v2_1_0_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_1_0]))
        if (APKTOOL_VERSION_2_2_1 in apktool_version):
            cmd_command.append(r'java -jar {0} d "{1}" -f -o {2}'.format(APKTOOL_v2_2_1_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_2_1]))

        if (APKTOOL_VERSION_2_3_3 in apktool_version): 
            cmd_command.append(r'java -jar {0} d "{1}" -f -o {2}'.format(APKTOOL_v2_3_3_NAME,apk_name,dest_dir[APKTOOL_VERSION_2_3_3]))



    print("cmd_command:"+str(cmd_command))
    print('=====================================================================')
    #执行命令
    for cmd in cmd_command:
        rmApktoolCache()
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print(line.decode("gbk"))
        print('=====================================================================')
        retval = p.wait()
        # p.kill()
        dir = cmd[cmd.rfind(' ')+1:]
        print('=======dir:',dir)
        generatePreVersion(dir)
        

    rmApktoolCache()

def generatePreVersion(dir):
        #delete apktool.yml and public.xml
        apktool_file = os.path.join(dir,'apktool.yml')
        public_file = os.path.join(dir,'res','values','public.xml')
        if(os.path.exists(apktool_file) and os.path.isfile(apktool_file)):
            os.remove(apktool_file)
        if(os.path.exists(public_file) and os.path.isfile(public_file)):
            os.remove(public_file)
        #modify AndroidManifest.xml
        manifest_file = os.path.join(dir,'AndroidManifest.xml')
        if(os.path.exists(manifest_file) and os.path.isfile(manifest_file)):
            ET.register_namespace(androidN, androidNS)
            tree = ET.parse(manifest_file)
            root = tree.getroot()
            # applicationCfg = ET.SubElement(root,'applicationCfg')
            permissionCfg = ET.SubElement(root,'permissionCfg')
            for use_permission in root.findall('uses-permission'):
                permissionCfg.append(use_permission)
                root.remove(use_permission)
            permissons = root.findall('permission')
            if permissons is not None:
                for permission in permissons:
                    permissionCfg.append(permission)
                    root.remove(permission)
            supports_screens = root.findall('supports-screens')
            if supports_screens is not None:
                for ss in supports_screens:
                    permissionCfg.append(ss)
                    root.remove(ss)

        application = root.find('application')
        print(application.tag)
        application.tag = 'applicationCfg'

        tree.write(manifest_file)
            
        # p  = subprocess.Popen("explorer "+ dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # p.wait()
        print('dir=========================='+dir)
        out_dir = os.path.join(APKTOOL_WORK_DIR,dir)
        print('out_dir======================='+out_dir)
        os.startfile(out_dir)
        
def rmApktoolCache():
    if os.path.isfile(APKTOOL_CACHE):
        os.remove(APKTOOL_CACHE)
        
if __name__ == "__main__":
    try:
        print('=====================================================================')
        apktool_version_AND_apkname = input("input apktool version,such as "+APKTOOL_VERSION_1_5_3 +","+APKTOOL_VERSION_2_0_1+","+APKTOOL_VERSION_2_2_1+","+APKTOOL_VERSION_2_0_3 +","+APKTOOL_VERSION_2_1_0 +","+APKTOOL_VERSION_2_3_3 +"or all:")
        apktool_version = apktool_version_AND_apkname.split(' ')[0]
        apk_name = apktool_version_AND_apkname.split(' ')[1]
        print("apktool_version is:" + apktool_version)
        print("target apk name is:" + apk_name)
        print('=====================================================================')

        dest_dir_1_5_3 = 'apk'+APKTOOL_VERSION_1_5_3+'\\'+apk_name.split("\\")[-1].split(".")[0].replace(' ','')
        dest_dir_2_0_1 = 'apk'+APKTOOL_VERSION_2_0_1+'\\'+apk_name.split("\\")[-1].split(".")[0].replace(' ','')
        dest_dir_2_0_3 = 'apk'+APKTOOL_VERSION_2_0_3+'\\'+apk_name.split("\\")[-1].split(".")[0].replace(' ','')
        dest_dir_2_1_0 = 'apk'+APKTOOL_VERSION_2_1_0+'\\'+apk_name.split("\\")[-1].split(".")[0].replace(' ','')
        dest_dir_2_2_1 = 'apk'+APKTOOL_VERSION_2_2_1+'\\'+apk_name.split("\\")[-1].split(".")[0].replace(' ','')
        dest_dir_2_3_3 = 'apk'+APKTOOL_VERSION_2_3_3+'\\'+apk_name.split("\\")[-1].split(".")[0].replace(' ','')
        dest_dir = {}
        if ('all' in apktool_version ):
            dest_dir[APKTOOL_VERSION_1_5_3] = dest_dir_1_5_3
            dest_dir[APKTOOL_VERSION_2_0_1] = dest_dir_2_0_1
            # dest_dir[APKTOOL_VERSION_2_0_3] = dest_dir_2_0_3
            # dest_dir[APKTOOL_VERSION_2_1_0] = dest_dir_2_1_0
            dest_dir[APKTOOL_VERSION_2_2_1] = dest_dir_2_2_1
            dest_dir[APKTOOL_VERSION_2_3_3] = dest_dir_2_3_3
        else:
            if (APKTOOL_VERSION_1_5_3 in apktool_version):
                dest_dir[APKTOOL_VERSION_1_5_3] = dest_dir_1_5_3
            if (APKTOOL_VERSION_2_0_1 in apktool_version):
                dest_dir[APKTOOL_VERSION_2_0_1] = dest_dir_2_0_1
            if (APKTOOL_VERSION_2_0_3 in apktool_version):
                dest_dir[APKTOOL_VERSION_2_0_3] = dest_dir_2_0_3
            if (APKTOOL_VERSION_2_1_0 in apktool_version):
                dest_dir[APKTOOL_VERSION_2_1_0] = dest_dir_2_1_0
            if (APKTOOL_VERSION_2_2_1 in apktool_version):
                dest_dir[APKTOOL_VERSION_2_2_1] = dest_dir_2_2_1
            if (APKTOOL_VERSION_2_3_3 in apktool_version): 
                dest_dir[APKTOOL_VERSION_2_3_3] = dest_dir_2_3_3
               

                    
        
        #execute decompiling
        print(dest_dir)
        print('=====================================================================')
        executeApktool(apktool_version,dest_dir)
        print('=====================================================================')
        
        input("press enter to exit")

    except Exception as e:
        #print("error:"+str(e))
        error_info = traceback.format_exc()
        print('error:'+error_info)
        input("press enter to exit")