from setuptools import setup
import analysis

setup(
    name=analysis.name,
    version=analysis.__version__,
    packages=['analysis'],
)
