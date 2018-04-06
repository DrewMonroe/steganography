# pystego
#### Drew Monroe

This is a fun project that I will probably use as a demonstration for a project for class.

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
