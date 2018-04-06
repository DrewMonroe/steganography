# pystego
#### Drew Monroe

## Description
This is a fun project that I will probably use as a demonstration for a project for class.
The idea is to use the least two significant bits of the `channel` image to hide a `secret` image.
Each pixel of the `secret` image is broken up into chunks of 2 bits each.
Then, we take one pixel of the `channel` image, and replace the lower two bits of that pixel with the first chunk of the `secret` image.
We then take the next pixel, and replace the lower two bits with the next chunk of the `secret` image.
The process continues until there are no more chunks, at which point the `channel` image is used to fill in the rest of the image.
This is NOT meant to be used for actual steganographic purposes, it's just a fun demo.

## Installation
```bash
pip install git+https://github.com/DrewMonroe/steganography.git#egg=pystego
```

## Usage
```bash
# To encode an image
encode_image --secret tux.png --channel crab_nebula.png --out hidden.png
# To decode an image
decode_image --encoded hidden.png --width 400 --height 400 --out recovered.png
```

## Limitations
- The script currently only hides one PNG inside of another.
- Both PNGs must have alpha values in order to process correctly
- Only the lower two bits of the `channel` image are used to hide the `secret` image.
There is currently no way to configure this.
If the `secret` image is too big, an exception will be raised instead of trying to use more bits.
