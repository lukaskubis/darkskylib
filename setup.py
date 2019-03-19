import os
from setuptools import setup

# use pandoc to convert
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst')) as f:
    README = f.read()

setup(name='darkskylib',
      version='0.3.91',
      description='The Dark Sky API wrapper',
      long_description=README,
      url='https://github.com/lukaskubis/darkskylib',
      author='Lukas Kubis',
      author_email='contact@lukaskubis.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
          'Topic :: Home Automation',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Operating System :: OS Independent',
      ],
      keywords='darksky dark-sky dark sky forecast home weather home-weather weather-station',
      packages=['darksky'],
      install_requires=[
          'future',
          'requests',
      ],
      test_suite='test',
      zip_safe=True
      )
