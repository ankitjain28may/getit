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


# ================================Error Function==========================
def usage():
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

def progressBar(length):
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


def transferRate(blocksize):
    try:
        global speed, rate, transferData
        interval = time() - rate
        if rate == 0:
            transferData += blocksize
            rate = time()
        elif interval == 0 or interval < 1:
            transferData += blocksize
        else:
            speed = float(transferData/(interval))
            transferData = 0
            rate = time()
        return speed
    except Exception:
        pass

# ================================Type of Data============================


def dataSize(block):
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


def reporthook(blocknum, blocksize, total):
    size = 0
    currentType = ''
    length = 30
    percentage = 100.00
    global speed, speedType, totalsize, sizeType
    desc = int(blocknum*blocksize)
    if total > 0:
        length = int((desc/total)*30)
        percentage = float(desc/total*100)
    speed = transferRate(blocksize)
    speedShow, speedType = dataSize(speed)
    if totalsize == 0:
        totalsize, sizeType = dataSize(total)
    size, currentType = dataSize(desc)
    progress = progressBar(length)

    if percentage > 100:
        percentage = 100
        size = totalsize
    elif percentage == 100 and total < 0:
        totalsize = size
    p1 = " %.2f %%" % (percentage)
    p2 = " %s" % (progress)
    p3 = " %.2f %s / %.2f %s %.2f %s/s   " % (
        size, currentType, totalsize, sizeType, speedShow, speedType)
    sys.stderr.write("\r" +
                     p1 + Fore.GREEN + p2 + Style.RESET_ALL + p3 + Style.RESET_ALL)
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
name = 'default'
opts = ''
args = ''
rate = 0
speed = 0
transferData = 0
totalsize = 0
speedType = ''
sizeType = ''
flag = 0
conf = ''
err = ''
path = "C:\\Users\\" + getuser() + "\\Downloads\\getit\\"
output, err = Commands(path, 'cd', True)
if err !='':
    Commands(path, 'mkdir')


# ================================Command Line Input======================

try:
    opts, args = getopt(
        argv, "hd:p:f:", ["help", "url=", "path=",  "filename="])
except GetoptError as err:
    usage()
    print(Fore.RED + str(err))
    sys.exit(2)

# ================================Read the CLI Input======================
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-d", "--url"):
        url = arg
    elif opt in ("-p", "--path"):
        path = arg
        path = pathCheck(path)
    elif opt in ("-f", "--filename"):
        name = arg
    else:
        usage()
        sys.exit(2)
if url == '':
    sys.stderr.write(
        Fore.GREEN + "? " + Style.RESET_ALL + "Enter the Download-Url : ")
    url = input()
    print(Fore.GREEN + "? " + Style.RESET_ALL +
          "URL : " + Fore.CYAN + url + Style.RESET_ALL)
if name == 'default':
    sys.stderr.write(Fore.GREEN + "? " + Style.RESET_ALL +
                     "File Name with extension : " + Fore.YELLOW + "(default) " + Style.RESET_ALL)
    name = input()
    if name == '':
        name = 'default'
    print(Fore.GREEN + "? " + Style.RESET_ALL +
          "Filename : " + Fore.CYAN + name + Style.RESET_ALL)
if path == "C:\\Users\\" + getuser() + "\Downloads\getit\\":
    sys.stderr.write(Fore.GREEN + "? " + Style.RESET_ALL +
                     "File Path : " + Fore.YELLOW + "(" + path + ") " + Style.RESET_ALL)
    path = input()
    if path == '':
        path = "C:\\Users\\" + getuser() + "\Downloads\getit\\"
    print(Fore.GREEN + "? " + Style.RESET_ALL +
          "Path : " + Fore.CYAN + path + Style.RESET_ALL)
    path = pathCheck(path)


# ================================Download the file=======================
try:
    name = nameAmend(name)
    print("Collecting " + name)
    print("\tDownloading... ")

    with open(path+name, 'wb') as out_file:
        with urlopen(url) as fp:
            x = int(fp.info()['Content-Length'])
            i=1
            block_size = 1024 * 8
            while True:
                block = fp.read(block_size)
                reporthook(i,block_size,x)
                i+=1
                if not block:
                    break
                out_file.write(block)

    # urlretrieve(url, path+name, reporthook)
    print("\n")
    print("Successfully download " + name)
    config = configparser.ConfigParser()
    if soft == "py":
        conf = 'config.cfg'
    else:
        conf, err = Commands('', 'which', True)
        if err!='':
            conf, err = Commands('', 'where getit.exe', True)
            conf = conf.split('\\')
            conf = conf[:-2]
            conf = '\\'.join(conf)
            conf+='\\config.cfg'
        else:
            conf, err = Commands('', 'which getit', True)
            conf = conf.split('\\')
            conf = conf[:-2]
            conf = '\\'.join(conf)
            conf+='\\config.cfg'
    try:
        sys.stdout.write("\a")
    except:
        pass
    config.read(conf)
    if config.getboolean('config-default', 'folder_open_on_download_complete'):
        Commands(path, 'start')
    if config.getboolean('config-default', 'file_open_on_download_complete'):
        Commands(path+name, 'start')
except Exception as e:
    print(Fore.RED + str(e))
