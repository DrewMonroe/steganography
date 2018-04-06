import argparse
import utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
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

    image_data = utils.encode(args.channel, args.secret)
    utils.writeImage(image_data, args.out)
