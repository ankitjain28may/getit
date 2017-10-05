import configparser
import subprocess
import sys
import platform
from getopt import GetoptError, getopt
from getpass import getuser
from time import time
from urllib.request import urlopen

from colorama import Fore, Style, init
init()


class Getit:
    def __init__(self, total):

        self.rate = 0
        self.speed = 0
        self.transferData = 0
        self.total = total
        self.totalsize, self.sizetype = self.datasize(total)
        self.speedtype = ''
        self.flag = 0

# ================================Progress Bar Function===================

    def progressbar(self, length):
        show = ''
        for _ in range(length):
            show += "#"
        for _ in range(30 - length):
            show += "-"
        show = "|" + show + "|"
        if length != 30:
            if length % 3 == 0:
                show = "/ " + show
            elif length % 3 == 1:
                show = "- " + show
            else:
                show = "\ " + show
        return show

    # ================================Transfer Speed Function=================

    def transferrate(self, blocksize):
        try:
            interval = time() - self.rate
            if self.rate == 0:
                self.transferData += blocksize
                self.rate = time()
            elif interval == 0 or interval < 1:
                self.transferData += blocksize
            else:
                self.speed = float(self.transferData / (interval))
                self.transferData = 0
                self.rate = time()
            return self.speed
        except Exception:
            pass

    # ================================Type of Data============================

    def datasize(self, block):
        if block / 1024 < 1000:
            block = block / 1024
            sizetype = 'KB'
        elif block / 1048576 < 1000:
            block = block / 1048576
            sizetype = 'MB'
        elif block / 1073741824 < 1000:
            block = block / 1073741824
            sizetype = 'GB'
        return block, sizetype

    # ================================Main Integrating function===============

    def reporthook(self, blocknum, blocksize):
        size = 0
        currenttype = ''
        length = 30
        percentage = 100.00
        desc = int(blocknum * blocksize)
        if self.total > 0:
            length = int((desc / self.total) * 30)
            percentage = float(desc / self.total * 100)
        self.speed = self.transferrate(blocksize)
        speedShow, self.speedtype = self.datasize(self.speed)
        size, currenttype = self.datasize(desc)
        progress = self.progressbar(length)

        if percentage > 100:
            percentage = 100
            size = self.totalsize
        elif percentage == 100 and self.totalsize < 0:
            self.totalsize = size
        p1 = " %.2f %%" % (percentage)
        p2 = " %s" % (progress)
        p3 = " %.2f %s / %.2f %s %.2f %s/s   " % (
            size, currenttype,
            self.totalsize,
            self.sizetype,
            speedShow,
            self.speedtype
        )
        sys.stderr.write(
            "\r" + p1 + Fore.GREEN + p2 + Style.RESET_ALL + p3 +
            Style.RESET_ALL
        )
        sys.stderr.flush()


# ================================Error Function==========================
def usage():

    logoname = """

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
    print(
        Fore.CYAN + logoname + Fore.YELLOW +
        "\b\b\bOptions: " + Fore.GREEN + usage
    )


# ================================Space separated name amendment==========


def nameamend(name):
    name = name.split(' ')
    name = '_'.join(name)
    return name

# ================================Path Check==============================


def commands(path, cmd, callback=False):
    try:
        if path != "" and cmd != "start":
            path = cmd + " \"" + path + "\""
        else:
            path = cmd + " " + path

        output, err = subprocess.Popen(
            path, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        ).communicate()

        if callback is not False:
            if err is not None:
                err = err.decode('utf-8')
            if output is not None:
                output = output.decode('utf-8')
            return output, err
    except Exception as e:
        usage()
        print(Fore.RED + str(e))
        sys.exit(2)


def pathcheck(path):
    _, err = commands(path, 'cd', True)
    if err != '':
        usage()
        print(Fore.RED + err)
        sys.exit(2)
    elif path[len(path) - 1] != '\\' or path[len(path) - 1] != "/":
        if platform.system() == "Windows":
            path += '\\'
        else:
            path += "/"
    return path


def main():

    # =====================================Globar Variables===================
    argv = sys.argv
    soft = argv[0].split('.')[-1]
    argv = argv[1:]
    url = ''
    opts = ''
    name = 'default'
    conf = ''
    err = ''
    presenttime = time()
    output = ''
    system = ''
    fname = ''
    info = ''
    if platform.system() == "Windows":  # for Windows
        path = "C:\\Users\\" + getuser() + "\\Downloads\\getit\\"
    elif platform.system() == "Darwin":  # for macOS
        path = "/Users/" + getuser() + "/Downloads/getit/"
    else:  # for linux
        path = "/home/" + getuser() + "/Downloads/getit/"
    output, err = commands(path, 'cd', True)
    if err != '':
        commands(path, 'mkdir')


# ================================Command Line Input======================
    try:
        opts, _ = getopt(
            argv, "hd:p:f:", ["help", "url=", "path=", "filename="])
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
            path = pathcheck(path)
        elif opt in ("-f", "--filename"):
            name = arg
        else:
            usage()
            sys.exit(2)
    if url == '':
        sys.stderr.write(
            Fore.GREEN + "? " + Style.RESET_ALL + "Enter the Download-Url : "
        )
        url = input()
        print(
            Fore.GREEN + "? " + Style.RESET_ALL +
            "URL : " + Fore.CYAN + url + Style.RESET_ALL
        )
    if name == 'default':
        sys.stderr.write(
            Fore.GREEN + "? " + Style.RESET_ALL +
            "File Name with extension : " + Fore.YELLOW +
            "(default) " + Style.RESET_ALL
        )
        name = input()
        if name == '':
            name = 'default'
        print(
            Fore.GREEN + "? " + Style.RESET_ALL +
            "Filename : " + Fore.CYAN + name + Style.RESET_ALL
        )
    if (path == "C:\\Users\\" + getuser() + "\Downloads\getit\\"
            or path == "/Users/" + getuser() + "/Downloads/getit/"
            or path == "/home/" + getuser() + "/Downloads/getit/"):
        sys.stderr.write(
            Fore.GREEN + "? " + Style.RESET_ALL +
            "File Path : " + Fore.YELLOW + "(" + path + ") " + Style.RESET_ALL
        )
        input_path = input()
        if input_path != '':
            path = input_path
        print(
            Fore.GREEN + "? " + Style.RESET_ALL +
            "Path : " + Fore.CYAN + path + Style.RESET_ALL
        )
        path = pathcheck(path)

    conf, err = commands('', 'which', True)
    if err != '':
        system = 'where'
        fname = ' getit.exe'
    else:
        system = 'which'
        fname = ' getit'
    output, err = commands(path + name, "dir", True)
    if err == '':
        sys.stderr.write(
            Fore.GREEN + "? " + Style.RESET_ALL + Fore.RED +
            "File already exists, overwrite?" + Fore.CYAN +
            " [Y/N] : " + Style.RESET_ALL
        )
        if input().upper() == 'N':
            print(
                Fore.RED +
                "\n\tAborted...!" + Style.RESET_ALL
            )
            sys.exit(2)


# ================================Download the file=======================
    try:
        name = nameamend(name)
        print("\nCollecting " + name)
        print("\tDownloading... ")
        with open(path + name, 'wb') as out_file:
            with urlopen(url) as fp:
                info = fp.info()
                if 'Content-Length' in info:
                    x = int(info['Content-Length'])
                else:
                    x = -1
                if x < 10000:
                    x = -1

                i = 1
                block_size = 1024 * 8
                ob = Getit(x)
                while True:
                    block = fp.read(block_size)
                    ob.reporthook(i, block_size)
                    i += 1
                    if not block:
                        break
                    out_file.write(block)

        print("\n")
        print("Successfully download " + name)
        config = configparser.ConfigParser()
        if soft == "py":
            conf = 'config.cfg'
        else:
            conf, err = commands('', system + fname, True)
            conf = conf.split('\\')
            conf = conf[:-1]
            conf = '\\'.join(conf)
            conf += '\\config.cfg'
        try:
            sys.stdout.write("\a")
        except Exception:
            pass
        print("\t Time Taken : %.2f sec" % (time() - presenttime))
        config.read(conf)
        if config.getboolean(
            'config-default',
            'folder_open_on_download_complete'
        ):
            commands(path, 'start')
        if config.getboolean(
            'config-default',
            'file_open_on_download_complete'
        ):
            commands(path + name, 'start')
    except Exception as e:
        print(Fore.RED + str(e))


if __name__ == '__main__':
    main()
