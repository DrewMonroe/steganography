from setuptools import setup, find_packages


setup(name='pystego',
      version='0.1',
      author="Drew Monroe",
      packages=find_packages(),
      install_requires=['Pillow', 'numpy', 'matplotlib'],
      scripts=['bin/encode_image',
               'bin/decode_image'
               'bin/analyze_images']
      )
