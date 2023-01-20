from setuptools import find_packages, setup


def read_file(file):
	with open(file, "r") as fh:
		return fh.read()


setup(
	name="manganelo",
	packages=find_packages(),
	version="1.23",
	license="MIT",

	description="Unofficial API for the Manganelo/Manganato website.",
	long_description=read_file("README.md"),
	long_description_content_type="text/markdown",

	author="Joshua Nixon",
	author_email="nixonjoshua98@gmail.com",

	url="https://github.com/nixonjoshua98/manganelo",

	download_url="https://github.com/nixonjoshua98/manganelo/releases",

	keywords=[
		"manga", "manganelo", "scrapper", "web", "mangakakalot", "thread", "comic", "manhwa", "manganato", "manhwa"
	],

	install_requires=[
		"bs4",
		"requests",
		"reportlab",
		"pillow",
		"pydantic"
	],

	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Build Tools",
	],

	python_requires='>=3.9'
)