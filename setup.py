from setuptools import find_packages, setup

setup(
    name="pythonic-notion-sdk",
    version="0.0.3",
    description="A pythonic way to interact with Notion without passing JSON around.",
    author="Florian Schaefer",
    author_email="florian.schaefer@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests==2.28.0"],
)
