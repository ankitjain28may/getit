import configparser
import subprocess
import sys
from getopt import GetoptError, getopt
from getpass import getuser
from time import time
from urllib.request import urlopen

from colorama import Fore, Style, init

from getit import Getit

init()


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
    elif path[len(path) - 1] != '\\':
        path += '\\'
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
    path = "C:\\Users\\" + getuser() + "\\Downloads\\getit\\"
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
    if path == "C:\\Users\\" + getuser() + "\Downloads\getit\\":
        sys.stderr.write(
            Fore.GREEN + "? " + Style.RESET_ALL +
            "File Path : " + Fore.YELLOW + "(" + path + ") " + Style.RESET_ALL
        )
        path = input()
        if path == '':
            path = "C:\\Users\\" + getuser() + "\Downloads\getit\\"
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
