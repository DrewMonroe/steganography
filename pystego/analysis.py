#!/usr/bin/env python3
import argparse
from pystego import utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze two PNGs'
                                                 ' detect steganographic'
                                                 ' information')
    parser.add_argument('image1', help='One of the two images')
    parser.add_argument('image2', help='The other image')

    args = parser.parse_args()

    utils.analyze(args.image1, args.image2)
