import os
import locale

import datetime as dt


def parse_date(s: str, _format: str):

	try:
		locale.setlocale(locale.LC_ALL, "en_US.UTF8")

		return dt.datetime.strptime(s, _format)

	finally:
		locale.setlocale(locale.LC_ALL, '')


def validate_path(path: str):
	dir_, file = os.path.split(path)

	for char in ("\\", "/", ":", "*", "?", "<", ">", "|"):
		file = file.replace(char, "")

	return os.path.join(dir_, file)