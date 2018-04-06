import binascii
import sys

import numpy
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


def hide(hideme, pixel, length=2):
    """Hides a two bit value inside of a pixel. Returns the new pixel"""
    return pixel[:-length] + hideme


def recover(pixel, length=2):
    """Recovers the 2 bits hidden in the pixel"""
    return pixel[-length:]


def encode(original, secret, size):
    """Encodes the secret image inside of the original image"""
    channel = Image.open(original)
    channel_pixels = channel.load()

    original_size = channel.size
    original_height = original_size[1]
    original_width = original_size[0]

    # The x and y coordinates of where we are in our images
    x = 0
    y = 0

    # TODO: Don't hardcode this
    channels = 4

    # The new image that we are creating
    new_image = numpy.zeros([original_height,
                             original_width,
                             channels],
                            dtype=numpy.uint8)
    # A row in the new image
    row = numpy.zeros([original_width, channels], dtype=numpy.uint8)

    # Iterate over the secret image and store the pixel values encoded in the
    # lowest two bits of each pixel in the old image

    secret_size = "{:032b}".format(size)
    for i in range(16):
        tmp = secret_size[2*i:2*i+2]
        tmp_pixel = pixel_to_bytes(channel_pixels[x, y])
        new_pixel = bytes_to_pixel(hide(tmp, tmp_pixel))
        row[x] = new_pixel
        x += 1

        if x >= original_width:
            x = 0
            new_image[y] = row
            y += 1

        if y >= original_height:
            raise Exception("Image too big")

    b = secret.read(1)
    while b:
        b = "{:08b}".format(int(b.hex(), 16))
        for i in range(4):
            tmp = b[2*i:2*i+2]
            tmp_pixel = pixel_to_bytes(channel_pixels[x, y])
            new_pixel = bytes_to_pixel(hide(tmp, tmp_pixel))
            row[x] = new_pixel
            x += 1

            if x >= original_width:
                x = 0
                new_image[y] = row
                y += 1

            if y >= original_height:
                raise Exception("Image too big")
        b = secret.read(1)

    # We've finished hiding our image in the original image, now we just need
    # to duplicate the rest of the original image

    # Iterate over the rest of the original image, setting the pixel value in
    # the new image to the exact value in the old image
    while y < original_height:
        while x < original_width:
            row[x] = channel_pixels[x, y]
            x += 1
        new_image[y] = row
        y += 1
        x = 0

    # Return our new image!
    return new_image


def decode(encoded_path):
    """Encodes the secret image inside of the original image"""
    encoded = Image.open(encoded_path)
    encoded_pixels = encoded.load()

    encoded_size = encoded.size
    encoded_width = encoded_size[0]

    # The x and y coordinates of where we are in our images
    x = 0
    y = 0

    # TODO: Don't hardcode this
    channels = 4

    # The new image that we are creating
    data = bytearray()

    size_str = ""
    for i in range(16):
        size_str += recover(pixel_to_bytes(encoded_pixels[x, y]))
        x += 1

        if x >= encoded_width:
            x = 0
            y += 1

    message_size = int(size_str, 2)
    print(message_size)
    i = 0

    data_chunk = ""
    while i < message_size:
        for j in range(4):
            data_chunk += recover(pixel_to_bytes(encoded_pixels[x, y]))
            x += 1

            if x >= encoded_width:
                x = 0
                y += 1

        data += int(data_chunk, 2).to_bytes(1, 'big')
        data_chunk = ""
        i += 1

    return data


def writeImage(np_array, file_path):
    """Writes a numpy array out to a file"""
    new_image = Image.fromarray(np_array)
    new_image.save(file_path)
