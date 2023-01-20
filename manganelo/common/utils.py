import os
import shutil
import locale
import typing
import datetime as dt
import html
import string
import ast
import contextlib as cl


def parse_number(number_string: str):
	with cl.suppress(Exception):
		return ast.literal_eval(number_string)

	number_string, unit = number_string[:-1], number_string[-1].upper()

	multiplier = {
		"B": 1_000_000_000,
		"M": 1_000_000,
		"K": 1_000
	}.get(unit, 1)

	with cl.suppress(Exception):
		return int(float(number_string) * multiplier)

	return -1




def unescape_html(s: str) -> str:
	return html.unescape(s).strip()


def split_at(s: str, sep: str) -> list[str]:
	return [x.strip() for x in s.split(sep)]


def encode_querystring(s: str) -> str:
	allowed_characters: str = string.ascii_letters + string.digits + "_"

	return "".join([char.lower() for char in s.strip().replace(" ", "_") if char in allowed_characters])


def save_image(image_data, path) -> typing.Union[str, None]:
	path = validate_path(path)

	with open(path, "wb") as fh:
		image_data.raw.decode_content = True

		# noinspection PyBroadException
		try:
			shutil.copyfileobj(image_data.raw, fh)

		except BaseException:
			return None

	return path


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
