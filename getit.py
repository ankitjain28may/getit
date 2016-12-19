from urllib.request import urlopen
from getopt import GetoptError, getopt
import sys
import subprocess
from getpass import getuser
from time import time
from colorama import Fore, Style
from colorama import init
import configparser
init()

class getit:
    def __init__(self, total):

        self.rate = 0
        self.speed = 0
        self.transferData = 0
        self.total = total
        self.totalsize, self.sizeType = self.dataSize(total)
        self.speedType = ''
        self.flag = 0


    # ================================Error Function==========================
    def usage(self):
        logoName = """

        ██████   ██████   ███████  ██   ███████       █████    █     █
        █        █           █     ██      █          █    █    █   █
        █        █           █     ██      █          █    █     █ █
        █  ███   ████        █     ██      █          █████       █
        █    █   █           █     ██      █          █           █
        █    █   █           █     ██      █          █           █
        ██████   ███████     █     ██      █     ██   █           █

        """
        usage = """
        -h, --help                 Print This
        -d, --url                  Download Url
        -p, --path                 Path to store the file
        -f, --filename             filename with extension

        """
        print(Fore.CYAN + logoName + Fore.YELLOW +
              "\b\b\bOptions: " + Fore.GREEN + usage)


    # ================================Progress Bar Function===================

    def progressBar(self,length):
        show = ''
        for i in range(length):
            show += "#"
        for j in range(30-length):
            show += "-"
        show = "|"+show+"|"
        if length != 30:
            if length % 3 == 0:
                show = "/ " + show
            elif length % 3 == 1:
                show = "- " + show
            else:
                show = "\ " + show
        return show

    # ================================Transfer Speed Function=================


    def transferRate(self,blocksize):
        try:
            interval = time() - self.rate
            if self.rate == 0:
                self.transferData += blocksize
                self.rate = time()
            elif interval == 0 or interval < 1:
                self.transferData += blocksize
            else:
                self.speed = float(self.transferData/(interval))
                self.transferData = 0
                self.rate = time()
            return self.speed
        except Exception:
            pass

    # ================================Type of Data============================


    def dataSize(self,block):
        if block/1024 < 1000:
            block = block/1024
            sizeType = 'KB'
        elif block/1048576 < 1000:
            block = block/1048576
            sizeType = 'MB'
        elif block/1073741824 < 1000:
            block = block/1073741824
            sizeType = 'GB'
        return block, sizeType

    # ================================Main Integrating function===============


    def reporthook(self,blocknum, blocksize):
        size = 0
        currentType = ''
        length = 30
        percentage = 100.00
        desc = int(blocknum*blocksize)
        if self.total > 0:
            length = int((desc/self.total)*30)
            percentage = float(desc/self.total*100)
        self.speed = self.transferRate(blocksize)
        speedShow, self.speedType = self.dataSize(self.speed)
        size, currentType = self.dataSize(desc)
        progress = self.progressBar(length)

        if percentage > 100:
            percentage = 100
            size = self.totalsize
        elif percentage == 100 and self.totalsize < 0:
            self.totalsize = size
        p1 = " %.2f %%" % (percentage)
        p2 = " %s" % (progress)
        p3 = " %.2f %s / %.2f %s %.2f %s/s   " % (
            size, currentType, self.totalsize, self.sizeType, speedShow, self.speedType
        )
        sys.stderr.write("\r" +
            p1 + Fore.GREEN + p2 + Style.RESET_ALL + p3 + Style.RESET_ALL
        )
        sys.stderr.flush()

# ================================Space separated name amendment==========


def nameAmend(name):
    name = name.split(' ')
    name = '_'.join(name)
    return name

# ================================Path Check==============================
def Commands(path, cmd, callback=False):
    try:
        path = cmd + " " + path
        output, err = subprocess.Popen(path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        if callback != False:
            if err!=None:
                err = err.decode('utf-8')
            if output!=None:
                output = output.decode('utf-8')
            return output, err
    except Exception as e:
        usage()
        print(Fore.RED + str(e))
        sys.exit(2)

def pathCheck(path):
    output, err = Commands(path, 'cd', True)
    if err!= '':
        usage()
        print(Fore.RED + err)
        sys.exit(2)
    elif path[len(path)-1] != '\\':
        path += '\\'
    return path


# =====================================Globar Variables===================

argv = sys.argv
soft = argv[0].split('.')[-1]
argv = argv[1:]
url = ''
opts = ''
args = ''
name = 'default'
conf = ''
err = ''
presentTime=time()
output = ''
System = ''
FNAME = ''
info = ''
path = "C:\\Users\\" + getuser() + "\\Downloads\\getit\\"
output, err = Commands(path, 'cd', True)
if err !='':
    Commands(path, 'mkdir')


# ================================Command Line Input======================

try:
    opts, args = getopt(
        argv, "hd:p:f:", ["help", "url=", "path=",  "filename="])
except GetoptError as err:
    getit().usage()
    print(Fore.RED + str(err))
    sys.exit(2)

# ================================Read the CLI Input======================
for opt, arg in opts:
    if opt in ("-h", "--help"):
        getit().usage()
        sys.exit()
    elif opt in ("-d", "--url"):
        url = arg
    elif opt in ("-p", "--path"):
        path = arg
        path = pathCheck(path)
    elif opt in ("-f", "--filename"):
        name = arg
    else:
        getit().usage()
        sys.exit(2)
if url == '':
    sys.stderr.write(
        Fore.GREEN + "? " + Style.RESET_ALL + "Enter the Download-Url : "
    )
    url = input()
    print(Fore.GREEN + "? " + Style.RESET_ALL +
        "URL : " + Fore.CYAN + url + Style.RESET_ALL
    )
if name == 'default':
    sys.stderr.write(Fore.GREEN + "? " + Style.RESET_ALL +
        "File Name with extension : " + Fore.YELLOW + "(default) " + Style.RESET_ALL
    )
    name = input()
    if name == '':
        name = 'default'
    print(Fore.GREEN + "? " + Style.RESET_ALL +
        "Filename : " + Fore.CYAN + name + Style.RESET_ALL
    )
if path == "C:\\Users\\" + getuser() + "\Downloads\getit\\":
    sys.stderr.write(Fore.GREEN + "? " + Style.RESET_ALL +
        "File Path : " + Fore.YELLOW + "(" + path + ") " + Style.RESET_ALL
    )
    path = input()
    if path == '':
        path = "C:\\Users\\" + getuser() + "\Downloads\getit\\"
    print(Fore.GREEN + "? " + Style.RESET_ALL +
        "Path : " + Fore.CYAN + path + Style.RESET_ALL
    )
    path = pathCheck(path)

conf, err = Commands('', 'which', True)
if err!='':
    System = 'where'
    FNAME = ' getit.exe'
else:
    System = 'which'
    FNAME = ' getit'
output, err = Commands(path+name, "dir", True)
if err == '':
    sys.stderr.write(Fore.GREEN + "? " + Style.RESET_ALL + Fore.RED +
        "File already exists, overwrite?"+ Fore.CYAN + " [Y/N] : " + Style.RESET_ALL
    )
    if input().upper() == 'N':
        print(Fore.RED +
            "\n\tAborted...!" + Style.RESET_ALL
        )
        sys.exit(2)


# ================================Download the file=======================
try:
    name = nameAmend(name)
    print("\nCollecting " + name)
    print("\tDownloading... ")
    with open(path+name, 'wb') as out_file:
        with urlopen(url) as fp:
            info = fp.info()
            if 'Content-Length' in info:
                x = int(info['Content-Length'])
            else:
                x = -1
            i=1
            block_size = 1024 * 8
            ob = getit(x)
            while True:
                block = fp.read(block_size)
                ob.reporthook(i,block_size)
                i+=1
                if not block:
                    break
                out_file.write(block)

    print("\n")
    print("Successfully download " + name)
    config = configparser.ConfigParser()
    if soft == "py":
        conf = 'config.cfg'
    else:
        conf, err = Commands('', System + FNAME , True)
        conf = conf.split('\\')
        conf = conf[:-2]
        conf = '\\'.join(conf)
        conf+='\\config.cfg'
    try:
        sys.stdout.write("\a")
    except:
        pass
    print("\t Time Taken : %.2f sec" %(time()-presentTime))
    config.read(conf)
    if config.getboolean('config-default', 'folder_open_on_download_complete'):
        Commands(path, 'start')
    if config.getboolean('config-default', 'file_open_on_download_complete'):
        Commands(path+name, 'start')
except Exception as e:
    print(Fore.RED + str(e))
