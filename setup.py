from setuptools import setup
import btc_analysis

setup(
    name=btc_analysis.name,
    version=btc_analysis.__version__,
    packages=['btc_analysis'],
    # test_suite="cryptoindex.tests"
)
