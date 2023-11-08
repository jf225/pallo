from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'A probablistic asset allocation model'
LONG_DESCRIPTION = 'A package that simplifies and streamlines the creation of probablistic allocation models. Primarily designed towards asset allocation the framework can theoretically work with any dataset. '

# Setting up
setup(
    name="pallo",
    version=VERSION,
    author="James Fahey",
    author_email="<jamesaf36@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['tqdm'],
    keywords=['python', 'finance', 'stocks', 'asset allocation', 'probabilities'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)