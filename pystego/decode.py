import argparse
from pystego import utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decode a hidden image')
    parser.add_argument('--encoded', '-e',
                        help='The encoded image',
                        required=True)
    parser.add_argument('--out', '-o',
                        help='The output file',
                        required=True)

    args = parser.parse_args()

    data = utils.decode(args.encoded)
    with open(args.out, 'wb') as f:
        f.write(data)
