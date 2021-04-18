import os
import shutil
import tempfile

from bs4 import BeautifulSoup

from PIL import Image

from reportlab.pdfgen import canvas

from manganelo.rewrite import utils, siterequests


class ChapterDownloader:
	def __init__(self, url):
		self._url = url

	def download(self, path):
		path = utils.validate_path(path)

		r = siterequests.get(self._url)

		soup = BeautifulSoup(r.content, "html.parser")

		urls = self._get_chapter_image_urls(soup)

		with tempfile.TemporaryDirectory() as dir_:
			images = self._download_images(dir_, urls)

			self._create_pdf(path, images)

		return path

	@staticmethod
	def _get_chapter_image_urls(soup):

		def valid(url: str):
			return url.endswith((".png", ".jpg"))

		return [url for url in map(lambda ele: ele["src"], soup.find_all("img")) if valid(url)]

	@staticmethod
	def _download_images(dir_, urls: list):
		images = []

		for i, url in enumerate(urls):
			image = siterequests.dl_image(url)

			if image is not None:
				ext = url.split(".")[-1]

				with open(os.path.join(dir_, f"{i}.{ext}"), "wb") as fh:
					image.raw.decode_content = True

					try:
						shutil.copyfileobj(image.raw, fh)

					except Exception as e:
						continue

					images.append(fh.name)

		return images

	@staticmethod
	def _create_pdf(path, images: list):

		pdf = canvas.Canvas(path)

		for image in images:
			try:
				with Image.open(image) as img:
					w, h = img.size

			except (OSError, UnboundLocalError):
				continue

			pdf.setPageSize((w, h))  # Set the page dimensions to the image dimensions

			pdf.drawImage(image, x=0, y=0)  # Insert the image onto the current page

			pdf.showPage()  # Create a new page ready for the next image

		pdf.save()