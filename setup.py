from setuptools import setup

setup(name='darkskylib',
      version='0.2.3',
      description='The Dark Sky API wrapper',
      url='https://github.com/lukaskubis/darkskylib',
      author='Lukas Kubis',
      author_email='contact@lukaskubis.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
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
          'Operating System :: OS Independent',
      ],
      keywords='darksky,dark sky,forecast,weather,home weather,weather station',
      packages=['darksky'],
      install_requires=[
          'requests',
          'future'
      ],
      zip_safe=False
      )
