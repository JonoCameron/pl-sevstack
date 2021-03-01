from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'sevstack',
    version          = '0.4',
    description      = 'A ChRIS plugin to produce ranked list of severity scores',
    long_description = readme,
    author           = 'Jonathan Cameron',
    author_email     = 'jacc@bu.edu',
    url              = 'http://wiki',
    packages         = ['sevstack'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'sevstack = sevstack.__main__:main'
            ]
        }
)
