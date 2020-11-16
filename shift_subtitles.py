# -*- coding: utf-8 -*-

import argparse

import pysrt

def shift(name, outname):
    subs = pysrt.open(name)
    subs.shift(seconds=5)
    subs.save(outname)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', help='subtitle file path')
    parser.add_argument('--outname', help='shifted subtitle file path')
    args = parser.parse_args()
    if args.file and args.outname:
        shift(args.file, args.outname)
    else:
        print (__doc__)