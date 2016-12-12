from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='smart-cameras',
    version=0.1,
    url='http://github.com/PedrosWits/smart-cameras',
    license='MIT License',
    author='Pedro Pinto da Silva',
    tests_require=['pytest'],
    install_requires=['azure>=2.0.0rc6',
                      'pytest-cov>=2.4.0',
                      'Sphinx>=1.5'],
    cmdclass={'test': PyTest},
    author_email='ppintodasilva@gmail.com',
    description='Smart Cameras using Azure',
    long_description=long_description,
    packages=['smart-cameras'],
    include_package_data=True,
    platforms='any',
    test_suite='smart-cameras.test.test_smart_cameras',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Smart Cities',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
