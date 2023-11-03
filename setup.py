from setuptools import setup

__package__ = "syn-flooder"
__version__ = "1.3.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name=__package__,
    version=__version__,
    author="cavoq",
    author_email="cavoq@proton.me",
    license="MIT License",
    description="SYN-Flooder Attack Tool for stress testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cavoq/syn-flooder",
    python_requires=">=3",
    py_modules=["syn_flooder"],
    scripts=["syn_flooder.py"],
    entry_points={
        "console_scripts": [
            "syn-flooder = syn_flooder:main",
        ],
    },
    install_requires=requirements,
)
