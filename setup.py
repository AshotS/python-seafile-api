from setuptools import setup, find_packages

__version__ = '0.1.3'


setup(name='seafileapi',
      version=__version__,
      license='BSD',
      description='Client interface for Seafile Web API',
      author='AshotS',
      platforms=['Any'],
      packages=find_packages(),
      install_requires=['requests'],
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'],
      )
