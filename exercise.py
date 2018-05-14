#!/usr/bin/env python
# coding: utf-8
import sys


def add(x, y):
    return x + y


if __name__ == '__main__':
    print(add(int(sys.argv[1]), int(sys.argv[2])))
