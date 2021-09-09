import os
import tempfile

from bs4 import BeautifulSoup

from PIL import Image

from reportlab.pdfgen import canvas

from manganelo import utils, siterequests


def download_chapter(url, path):
	path = utils.validate_path(path)

	r = siterequests.get(url)

	soup = BeautifulSoup(r.content, "html.parser")

	urls = _get_image_urls_from_soup(soup)

	with tempfile.TemporaryDirectory() as dir_:
		if images := _download_images(dir_, urls):
			_create_pdf(path, images)

	return path


def _get_image_urls_from_soup(soup):

	def valid(url: str):
		return url.endswith((".png", ".jpg"))

	return [url for url in map(lambda ele: ele["src"], soup.find_all("img")) if valid(url)]


def _download_images(dir_, urls: list):
	images = []

	for i, url in enumerate(urls):
		image = siterequests.get_image(url)

		if image is not None:
			ext = url.split(".")[-1]

			path = utils.save_image(image, os.path.join(dir_, f"{i}.{ext}"))

			if path:
				images.append(path)

	return images


def _create_pdf(path, images: list):
	pdf = canvas.Canvas(path)

	for image in images:

		# noinspection PyBroadException
		try:
			with Image.open(image) as img:
				w, h = img.size

		except BaseException:
			continue

		pdf.setPageSize((w, h))  # Set the page dimensions to the image dimensions

		pdf.drawImage(image, x=0, y=0)  # Insert the image onto the current page

		pdf.showPage()  # Create a new page ready for the next image

	pdf.save()