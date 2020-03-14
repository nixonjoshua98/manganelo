from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name="manganelo",
  packages=find_packages(),
  version="1.2",
  license="MIT",

  long_description_content_type="text/markdown",

  description="Unofficial API for the Manganelo (and Mangakakalot) website.",
  long_description=long_description,

  author="Joshua Nixon",
  author_email="nixonjoshua98@gmail.com",

  url="https://github.com/nixonjoshua98/manganelo",

  download_url="https://github.com/nixonjoshua98/manganelo/archive/v1.2.tar.gz",
  
  keywords=["manga", "manganelo", "scrapper", "web", "mangakakalot"],
  
  install_requires=[
    "bs4",
    "requests",
  ],

  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",  
    "Topic :: Software Development :: Build Tools",
  ],

  python_requires='>=3.7'
)
