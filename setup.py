import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hashver",
    version="0.0.2",
    author="Ashutosh Kumar",
    author_email="ashutoshk.akumar@gmail.com",
    description=(
        "hashver is a python module to derive a unique numeric value from a"
        " version string and vice versa"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashutoshkumr/python-hashver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
