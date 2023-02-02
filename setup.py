from setuptools import setup

setup(
    name="PytomatedLiquidHandling",
    version="3.0",
    packages=["PytomatedLiquidHandling"],
    license="MIT",
    description="Python for labware automation",
    install_requires=["xlwings", "pyyaml", "web.py"],
    url="https://github.com/Pfizer-BradleyBare/PytomatedLiquidHandling.git",
    author="Bradley Bare",
    author_email="Bradley.Bare@pfizer.com",
)
