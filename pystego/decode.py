import argparse
from pystego import utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decode a hidden image')
    parser.add_argument('--encoded', '-e',
                        help='The encoded image',
                        required=True)
    parser.add_argument('--width', '-W',
                        help='The width of the new image',
                        type=int,
                        required=True)
    parser.add_argument('--height', '-H',
                        help='The height of the new image',
                        type=int,
                        required=True)
    parser.add_argument('--out', '-o',
                        help='The output file',
                        required=True)

    args = parser.parse_args()

    image_data = utils.decode(args.encoded, args.width, args.height)
    utils.writeImage(image_data, args.out)
