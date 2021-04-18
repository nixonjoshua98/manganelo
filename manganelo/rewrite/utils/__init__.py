import os
import locale

import datetime as dt


def parse_date(s: str, _format: str):

	try:
		# Standardize locale to match foreign language
		locale.setlocale(locale.LC_ALL, "en_US.UTF8")

		date = dt.datetime.strptime(s, _format)

	finally:
		# Rese-set the locale
		locale.setlocale(locale.LC_ALL, '')

	return date


def validate_path(path: str):
	dir_, file = os.path.split(path)

	for char in ("\\", "/", ":", "*", "?", "<", ">", "|"):
		file = file.replace(char, "")

	return os.path.join(dir_, file)