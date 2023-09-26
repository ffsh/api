""" setup file """
from setuptools import setup, find_packages


with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='apiupdater',
    version='0.0.2',
    description='Updates your Freifunk API File',
    long_description=README,
    author='Benjamin Brahmer',
    author_email='info@b-brahmer.de',
    url='https://github.com/ffsh/api/tree/main',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'apiupdater = apiupdater.apiupdater:main'
        ]
    }
)
