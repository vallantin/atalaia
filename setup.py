from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Atalaia",
    version="0.2.0",
    author="Lima Vallantin",
    author_email="lima@vallant.in",
    description="Atalaia is a collection of methods that can be used for simple NLP tasks and for machine learning text preprocessing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vallantin/atalaia",
    license="Apache",
    packages=find_packages()
)
