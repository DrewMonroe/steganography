import os

import argparse
from pystego import utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hide one PNG in another')
    parser.add_argument('--secret', '-s',
                        help='The image you want to be secret',
                        required=True)
    parser.add_argument('--channel', '-c',
                        help='The image you to encode the secret in',
                        required=True)
    parser.add_argument('--out', '-o',
                        help='The output file',
                        required=True)

    args = parser.parse_args()

    size = os.path.getsize(args.secret)
    with open(args.secret, 'rb') as f:
        image_data = utils.encode(args.channel, f, size)
    utils.writeImage(image_data, args.out)
