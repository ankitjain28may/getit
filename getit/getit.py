import sys
from time import time

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
