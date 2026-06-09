import os
import pathlib

from setuptools import setup

import codenerix_lib

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()


def _read_requirements(path):
    """Loose direct deps from requirements.in (never the compiled lock)."""
    return [
        line.strip()
        for line in pathlib.Path(path).read_text().splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "-"))
    ]


install_requires = _read_requirements("requirements.in")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="codenerix_lib",
    version=codenerix_lib.__version__,
    packages=["codenerix_lib"],
    include_package_data=True,
    zip_safe=False,
    package_data={
        "codenerix_lib": ["py.typed"],
    },
    license="Apache License Version 2.0",
    description="Basic libraries used by CODENERIX.",
    long_description=README,
    url="https://github.com/codenerix/codenerix-lib",
    author=", ".join(codenerix_lib.__authors__),
    author_email=", ".join(codenerix_lib.__authors_email__),
    keywords=["codenerix"],
    platforms=["OS Independent"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=install_requires,
)
