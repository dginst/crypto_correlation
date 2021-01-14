from setuptools import setup
import btc_analysis

setup(
    name=btc_analysis.name,
    version=btc_analysis.__version__,
    packages=['btc_analysis'],
    # test_suite="cryptoindex.tests"
)

# setuptools.setup(
#     name="example-pkg-YOUR-USERNAME-HERE",  # Replace with your own username
#     version="0.0.1",
#     author="Example Author",
#     author_email="author@example.com",
#     description="A small example package",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )
