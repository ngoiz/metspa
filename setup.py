from setuptools import find_packages, setup

setup(
    name="metspa",
    packages=find_packages(
        where="./",
        include=["metspa*"],
        exclude=["tests"],
    ),
    entry_points={"console_scripts": ["metspa=metspa.main:main"]},
)
