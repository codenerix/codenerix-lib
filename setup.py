import os
from setuptools import setup

import codenerix_lib

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='codenerix-lib',
    version=codenerix_lib.__version__,
    packages=["codenerix_lib"],
    include_package_data=True,
    zip_safe=False,
    license='Apache License Version 2.0',
    description='Basic libraries used by CODENERIX.',
    long_description=README,
    url='https://github.com/codenerix/codenerix-lib',
    author=", ".join(codenerix_lib.__authors__),
    keywords=['codenerix'],
    platforms=['OS Independent'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'pycryptodomex',
        'colorama',
    ]
)
