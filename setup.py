from setuptools import setup, find_packages
import os

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


VERSION = "0.0.2"
DESCRIPTION = "Cloudflare AI Python SDK"


setup(
    name="cloudflare-ai",
    author="alexraskin",
    description=DESCRIPTION,
    version=VERSION,
    url="https://github.com/alexraskin/cloudflare-ai-py",
    author_email="<root@alexraskin.com",
    license="MIT License",
    keywords=["module", "Cloudflare", "library", "package", "python", "CloudflareAI"],
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    install_requires=["httpx", "aiofiles", "starlette", "Pillow"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ],
)
