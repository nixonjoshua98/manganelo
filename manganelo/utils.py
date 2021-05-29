import locale


from datetime import datetime


def parse_date(s: str, _format: str):

	try:
		# Standardize locale to match foreign language
		locale.setlocale(locale.LC_ALL, "en_US.UTF8")

		date = datetime.strptime(s, _format)

	finally:
		# Rese-set the locale
		locale.setlocale(locale.LC_ALL, '')

	return date
