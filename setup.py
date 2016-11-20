from setuptools import setup, find_packages
from codecs import open
import os


here = os.path.abspath(os.path.dirname(__file__))

exec(open(os.path.join(here, "cheat_ext", "version.py")).read())

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cheat-ext",
    version=globals()["VERSION"],
    description="Cheat Extension",
    long_description=long_description,
    author="chhsiao90",
    author_email="chhsiao90@gmail.com",
    url="https://github.com/chhsiao90/cheat-ext",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages(include=["cheat_ext", "cheat_ext.*"]),
    test_suite="cheat_ext.tests",
    entry_points={
        "console_scripts": [
            "cheat-ext=cheat_ext.main:main",
        ],
    },
    install_requires=[
        "GitPython==2.1.0",
    ],
    extras_require={
        "dev": [
            "mock==2.0.0",
            "tox==2.5.0",
            "pytest==3.0.4",
        ],
    },
)
