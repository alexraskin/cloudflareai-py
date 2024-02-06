import os
from re import MULTILINE, search

from setuptools import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version = ""
with open("cloudflareai/__init__.py") as f:
    version = search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Unable to find version string.")

setup(
    name="cloudflareai",
    author="alexraskin",
    description="Cloudflare AI Python SDK",
    version=version,
    url="https://github.com/alexraskin/cloudflareai-py",
    author_email="<root@alexraskin.com>",
    license="Mozilla Public License 2.0",
    keywords=["module", "Cloudflare", "library", "package", "python", "CloudflareAI"],
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    install_requires=["httpx"],
    packages=["cloudflareai"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
    ],
)
