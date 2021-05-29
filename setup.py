from setuptools import setup, find_packages


def read_file(file):
	with open(file, "r") as fh:
		return fh.read()


setup(
	name="manganelo",
	packages=find_packages(),
	version="dev",
	license="MIT",

	description="Unofficial API for the Manganelo website.",
	long_description=read_file("README.md"),
	long_description_content_type="text/markdown",

	author="Joshua Nixon",

	url="https://github.com/nixonjoshua98/manganelo",

	install_requires=[
		"bs4",
		"requests",
		"reportlab",
		"pillow"
	],

	python_requires='>=3.7'
)
