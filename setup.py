from setuptools import setup


setup(
    name="pythonic-notion-api",
    version="0.0.2",
    description="A pythonic way to interact with Notion without passing JSON around.",
    author="Florian Schaefer",
    author_email="florian.schaefer@gmail.com",
    license="MIT",
    packages=["notion"],
    install_requires=["requests==2.28.0"],
)
