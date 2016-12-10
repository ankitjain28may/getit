from urllib.request import urlretrieve
from getopt import GetoptError, getopt
import sys, os
from getpass import getuser
from time import time
from colorama import Fore, Style
from colorama import init
init()


# ================================Error Function=========================================
def usage():
    print(Fore.YELLOW + "\n\t==========Invalid Input=============")
    usage = """
    -h --help                 Print This
    -d --url                  Download Url
    -p --path                 Path to store the file
    -f --filename             filename with extension
    """
    print(usage)
    print("\n\t===============End==================")


# ================================Progress Bar Function=========================================

def progressBar(length):
    show = ''
    for i in range(length):
        show+="#"
    for j in range(50-length):
        show+="-"
    show = "["+show+"]"
    if length!=50:
        if length % 3 == 0:
            show = "/ " + show
        elif length % 3 == 1:
            show = "- " + show
        else:
            show = "\ " + show
    return show

# ================================Transfer Speed Function=========================================

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

# ================================Type of Data=========================================

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

# ================================Main Integrating function=========================================

def reporthook(blocknum, blocksize, total):
    size = 0
    currentType = ''
    desc = int(blocknum*blocksize)
    length = int((desc/total)*50)
    percentage = float(desc/total*100)
    global speed, speedType, totalsize, sizeType
    speed = transferRate(blocksize)
    speedShow, speedType = dataSize(speed)
    if totalsize == 0:
        totalsize, sizeType = dataSize(total)
    size, currentType = dataSize(desc)
    progress = progressBar(length)

    if percentage > 100:
        percentage = 100
        size = totalsize
    p1 = "\r %.2f %% " %(percentage)
    p2 = "%s " %(progress)
    p3 = "%.2f %s / %.2f %s %.2f %s/sec " %(size, currentType, totalsize, sizeType, speedShow, speedType)
    sys.stderr.write(p1 + Fore.GREEN + p2)
    sys.stderr.write(Style.RESET_ALL)
    sys.stderr.write(p3)
    sys.stderr.write(Style.RESET_ALL)
    sys.stdout.flush()

# ================================Space separated name amendment=========================================

def nameAmend(name):
    name = name.split(' ')
    name = '_'.join(name)
    return name

def pathCheck(path):
    if not os.path.exists(path):
        usage()
        print(Fore.RED + str("Path is not found"))
        sys.exit(2)
    elif path[len(path)-1] != '\\':
        path+='\\'
    return path
# =====================================Globar Variables=========================================

argv = sys.argv[1:]
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
path = "C:\\Users\\" + getuser() + "\Downloads\getit\\"
if not os.path.exists(path):
    os.mkdir(path)

# ================================Command Line Input=====================================

try:
    opts, args = getopt(argv, "hd:p:f:", ["help", "url=", "path=",  "filename="])
except GetoptError as err:
    usage()
    print(Fore.RED + str(err))
    sys.exit(2)

# ================================Read the CLI Input=====================================
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
    url = input("Enter the Download-Url\n")
if name == 'default':
    name = input("Enter the name of the File with the extension\n")
if path == "C:\\Users\\" + getuser() + "\Downloads\getit\\":
    path = input("Enter the path to store the file\n")
    if path == '':
        path = "C:\\Users\\" + getuser() + "\Downloads\getit\\"
    path = pathCheck(path)

# ================================Download the file======================================
try:
    name = nameAmend(name)
    print("Downloading starts...\n")
    urlretrieve(url, path+name, reporthook)
    print("\n")
    print("Download completed..!!\n")
except Exception as e:
    print(Fore.RED + str(e))

