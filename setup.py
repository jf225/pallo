from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.0'
DESCRIPTION = 'Simplifies the creation and usage of probabilistic asset allocation models'
#LONG_DESCRIPTION = 'A package that simplifies and streamlines the creation of probablistic allocation models. Primarily designed towards asset allocation the framework can theoretically work with any dataset. To view more inforamtion, uses, and package discription go to the github repository: https://github.com/jf225/pallo'

# Setting up
setup(
    name="pallo",
    version=VERSION,
    author="James Fahey",
    author_email="<jamesaf36@gmail.com>",
    url='https://github.com/jf225/pallo',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['tqdm >= 4.64.0', 'numpy >= 1.26.1', 'scipy >= 1.7.3', 'yfinance >= 0.2.14', 'pandas-datareader >= 0.10.0'],
    license="MIT",
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
