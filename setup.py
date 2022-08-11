from setuptools import setup, find_packages
import re
import os

setup(
    name='metspa',
    packages=find_packages(
        where='./',
        include=['metspa*'],
        exclude=['tests'],
    ),
    entry_points={
        'console_scripts': ['metspa=metspa.main:main']
    }
)
