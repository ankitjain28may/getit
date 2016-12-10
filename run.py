import urllib.request
import requests
import sys, getopt
import time
from colorama import Fore, Style
from colorama import init
init()
# ================================Error Function=========================================
def usage():
    print("\n\t==========Invalid Input=============")
    usage = """
    -h --help                 Print This
    -d --url                  Download Url
    -f --filename             filename with extension
    """
    print(usage)
    print("\n\t===============End==================")

def progressBar(length):
    show = ''
    # return length
    for i in range(length):
        show+="#"
    for j in range(50-length):
        show+="-"
    return "["+show+"]"

def transferRate(blocksize):
    try:
        global speed, t, transferData
        interval = time.time() - t
        if t == 0:
            transferData += blocksize
            t = time.time()
        elif interval == 0 or interval < 1:
            transferData += blocksize
        else:
            speed = float(transferData/(interval))
            transferData = 0
            t = time.time()
        return speed
    except Exception:
        pass

def dataSize(block):
    if block/1024 < 1000:
        block = block/1024
        factor = 1
        sizeType = 'KB'
    elif block/1048576 < 1000:
        block = block/1048576
        factor = 2
        sizeType = 'MB'
    elif block/1073741824 < 1000:
        block = block/1073741824
        factor = 3
        sizeType = 'GB'
    return block, factor, sizeType


def reporthook(blocknum, blocksize, totalsize):
    desc = int(blocknum*blocksize)
    sizeType = ''
    size = 0
    factor = 0
    length = int(desc/totalsize*50)
    percentage = float(desc/totalsize*100)
    global speed, speedData
    speed = transferRate(blocksize)
    speedShow, factor, speedData = dataSize(speed)
    totalsize, factor, sizeType = dataSize(totalsize)
    if factor == 1:
        size = float(desc/1024)
    elif factor == 2:
        size = float(desc/1048576)
    elif factor == 3:
        size = float(desc/1073741824)

    if percentage > 100:
        percentage = 100
        size = totalsize
    progress = progressBar(length)
    # s = "\r%.2f %% %s %.2f %s / %.2f %s %.2f %s/sec " % (percentage, progress, size, sizeType, totalsize, sizeType, speedShow, speedData)
    p1 = "\r %.2f %% " %(percentage)
    p2 = "%s " %(progress)
    p3 = "%.2f %s / %.2f %s %.2f %s/sec " %(size, sizeType, totalsize, sizeType, speedShow, speedData)
    sys.stdout.flush()
    sys.stderr.write(p1 + Fore.GREEN + p2)
    sys.stderr.write(Style.RESET_ALL)
    sys.stderr.write(p3)
    sys.stderr.write(Style.RESET_ALL)
    sys.stdout.flush()

def nameAmend(name):
    name = name.split(' ')
    name = '_'.join(name)
    return name

# =====================================Main Body=========================================

argv = sys.argv[1:]
url = ''
name = 'default'
opts = ''
args = ''
t = 0
speed = 0
speedData = ''
transferData = 0
# ================================Command Line Input=====================================

try:
    opts, args = getopt.getopt(argv, "hd:f:", ["help", "url=", "filename="])
except getopt.GetoptError as err:
    usage()
    print(str(err))
    sys.exit(2)
# ================================Read the CLI Input=====================================
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-d", "--url"):
        url = arg
    elif opt in ("-f", "--filename"):
        name = arg
    else:
        usage()
        sys.exit(2)
if url == '':
    url = input("Enter the Download-Url\n")
if name == 'default':
    name = input("Enter the name of the File with the extension\n")
# ================================Download the file======================================
try:
    name = nameAmend(name)
    print("Downloading starts...\n")
    urllib.request.urlretrieve(url, name, reporthook)
    print("\n")
    print("Download completed..!!\n")
except Exception as e:
    print(e)

