from distutils.core import setup

setup(
  name="manganelo",
  packages=["manganelo"],
  version="0.3",
  license="MIT",

  description="Unofficial API for the Manganelo (and Mangakakalot) website.",
  long_description="Unofficial API for the Manganelo (and Mangakakalot) website.",

  author="Joshua Nixon",
  author_email="nixonjoshua98@gmail.com",

  url="https://github.com/nixonjoshua98/manganelo-api",

  download_url="https://github.com/nixonjoshua98/manganelo-api/archive/v0.3.tar.gz",
  
  keywords=["manga", "manganelo", "scrapper", "web", "mangakakalot"],
  
  install_requires=[
    "bs4",
    "requests"
  ],

  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
  
  classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",  
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
  ],
)
