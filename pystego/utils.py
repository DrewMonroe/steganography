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


def encode(original, secret):
    """Encodes the secret image inside of the original image"""
    channel = Image.open(original)
    channel_pixels = channel.load()

    secret = Image.open(secret)
    secret_pixels = secret.load()

    original_size = channel.size
    original_height = original_size[1]
    original_width = original_size[0]

    secret_size = secret.size
    secret_height = secret_size[1]
    secret_width = secret_size[0]

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

    # Iterate over the height of the secret image
    for h in range(secret_height):
        # Iterate over the width of the secret image
        for w in range(secret_width):
            # Get the secret pixel at the given width and height that we are at
            s = pixel_to_bytes(secret_pixels[w, h])
            # We encode the 32 bit number that represents a pixel two bits at
            # a time, so iterate over pairs of bits
            # TODO: Don't hardcode 16?
            for i in range(16):
                # If the location that we would write a bit to is outside of
                # the bounds of our original image, wrap to the next line of
                # the new image
                if x >= original_width:
                    x = 0
                    # Set the row of the new image to the row that we created
                    new_image[y] = row
                    y += 1
                # If y is too big, the original image isn't large enough to
                # hold all of the secret data. We'd need to use more than
                # 2 bits
                if y >= original_height:
                    raise Exception("Image too big")

                # Convert the current pixel in the original to a bytestring
                c = pixel_to_bytes(channel_pixels[x, y])
                # Change the last two bits of the original pixel to hold our
                # data
                hidden = bytes_to_pixel(hide(s[2*i:2*i+2], c))
                # Set the given pixel in the row to hold our modified pixel
                row[x] = hidden
                x += 1

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


def writeImage(np_array, file_path):
    """Writes a numpy array out to a file"""
    new_image = Image.fromarray(np_array)
    new_image.save(file_path)
