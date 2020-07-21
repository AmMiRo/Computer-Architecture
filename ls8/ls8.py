#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

def run_cpu(file):
    cpu = CPU()
    cpu.load(file)
    cpu.run()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please include a program to run Ex: python3 ls8.py <program to run>")
    else:
        run_cpu(sys.argv[1])
