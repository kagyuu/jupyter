#!/usr/bin/env python
# coding: utf-8

"""
Create numpy formatted Orthogonal Arrays from text file.

This program create a hdf5 file contains many arrays.
These arrays are came from :
http://support.sas.com/techsup/technote/ts723_Designs.txt
"""
__author__ = "HONDOH Atsushi <kagyuu@hondou.homedns.org>"
__version__ = "1.00"
__date__ = "June 28 2018"

import h5py
import re
import numpy as np
from typing import List, Any


def read_header(line):
    header = line.split("n=")

    name = header[0].strip()
    rows = header[1].strip()

    cols: List[tuple[Any]] = []
    for col in name.split(" "):
        cols.append(tuple(col.split("^")))

    return name, rows, cols


def save_matrix(name, matrix, fd):
    print(name)
    print(np.array(matrix))
    fd.create_dataset(name, data=np.array(matrix))


def main():
    test_data = open("ts723_Designs.txt", "r")
    hdf5 = h5py.File("oamatrix.hdf5", 'w')
    lines = test_data.readlines()

    count = 0
    name = ""
    rows = ""
    cols = []
    matrix = None
    for line in lines:

        # this line is blank line
        if len(line.strip()) == 0:
            continue

        # this line is matrix header line, like as "2^12 12^1     n=24"
        if re.match(".*n=[0-9]+", line):
            if matrix is not None:
                save_matrix(name, matrix, hdf5)

            name, rows, cols = read_header(line)
            matrix = list()
            count += 1
            continue

        # this line is matrix row line, like as "101101000111 3"
        # convert this line to an array
        ary = []
        p = 0
        for col in cols:
            # the col is "s^n"
            s = col[0]
            n = col[1]
            # If col < 10 then this col is defined in 1 digit.
            # Because {0,1,2,3,4,5,6,7,8,9}
            digit: int = 1 if int(s) <= 10 else 2
            for cnt in range(0, int(n)):
                ary.append(int(line[p: p + digit]))
                p += digit

        matrix.append(ary)

    # save the last matrix
    # Because this program module save matrix each when the header of matrix were found.
    if matrix is not None:
        save_matrix(name, matrix, hdf5)

    test_data.close()

    hdf5.flush()
    hdf5.close()


if __name__ == '__main__':
    main()
