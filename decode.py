import numpy
import argparse
from PIL import Image


def pixel_to_bytes(p):
    """Takes a pixel (a tuple) and turns it into a byte string"""
    # TODO: Deal with PNGS with non-alpha pixel values in them
    return "{:032b}".format(256**3 * p[0] +
                            256**2 * p[1] +
                            256**1 * p[2] +
                            256**0 * p[3])


def bytes_to_pixel(b):
    """Takes a byte string and turns it into a tuple of pixel data"""
    b0 = int(b[0:8], 2)
    b1 = int(b[8:16], 2)
    b2 = int(b[16:24], 2)
    b3 = int(b[24:32], 2)

    return (b0, b1, b2, b3)


def recover(pixel, length=2):
    """Hides a two bit value inside of a pixel. Returns the new pixel"""
    return pixel[-length:]


def decode(encoded_path, width, height):
    """Encodes the secret image inside of the original image"""
    encoded = Image.open(encoded_path)
    encoded_pixels = encoded.load()

    encoded_size = encoded.size
    encoded_height = encoded_size[1]
    encoded_width = encoded_size[0]

    # The x and y coordinates of where we are in our images
    x = 0
    y = 0

    # TODO: Don't hardcode this
    channels = 4

    # The new image that we are creating
    new_image = numpy.zeros([height,
                             width,
                             channels],
                            dtype=numpy.uint8)
    # A row in the new image
    row = numpy.zeros([width, channels], dtype=numpy.uint8)
    tmp_pixel = ""

    done = False

    # Iterate over the secret image and store the pixel values encoded in the
    # lowest two bits of each pixel in the old image

    # Iterate over the height of the secret image
    for h in range(encoded_height):
        # Iterate over the width of the secret image
        for w in range(encoded_width):
            p = pixel_to_bytes(encoded_pixels[w, h])
            hidden = recover(p)
            tmp_pixel += hidden

            # TODO: This probably won't be 32 if no A values
            if len(tmp_pixel) == 32:
                row[x] = bytes_to_pixel(tmp_pixel)
                x += 1
                tmp_pixel = ""
            if x == width:
                new_image[y] = row
                x = 0
                y += 1
            if y == height:
                done = True
                break
        if done is True:
            break

    # Return our new image!
    return new_image


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

    image_data = decode(args.encoded, args.width, args.height)
    new_image = Image.fromarray(image_data)
    new_image.save(args.out)
