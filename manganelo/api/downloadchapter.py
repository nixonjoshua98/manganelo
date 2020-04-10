import os
import shutil
import tempfile
import typing

from bs4 import BeautifulSoup
from PIL import Image
from reportlab.pdfgen import canvas

from manganelo import utils


class DownloadChapter:
	def __init__(self, src_url: str, dst_path: str):
		super().__init__()

		self.ok = False

		self._src_url = src_url
		self._dst_path = dst_path

		self._download_chapter()

	def _download_chapter(self):
		response = utils.send_request(self._src_url)

		# Entire page soup
		soup = BeautifulSoup(response.content, "html.parser")

		if soup is None:
			raise Exception("Request failed")

		image_urls = self._get_image_urls(soup)

		with tempfile.TemporaryDirectory() as temp_dir:
			image_paths = self._download_images(image_urls, temp_dir)

			self._create_pdf(image_paths)

	@staticmethod
	def _get_image_urls(soup) -> typing.List[str]:
		image_soup = soup.find_all("img")

		image_urls = [ele["src"] for ele in image_soup]

		return image_urls

	def _create_pdf(self, images: typing.List[str]):
		pdf = canvas.Canvas(self._dst_path)

		for image in images:
			try:
				with Image.open(image) as img:
					w, h = img.size

			except (OSError, UnboundLocalError):
				continue

			pdf.setPageSize((w, h))

			try:
				pdf.drawImage(image, x=0, y=0)

			except OSError as e:
				continue

			pdf.showPage()

		pdf.save()

		self.ok = True

	def _download_images(self, image_urls: typing.List[str], save_dir: str) -> typing.List[str]:
		image_paths = []

		for i, url in enumerate(image_urls):
			image = utils.send_request(url)
			image_ext = url.split(".")[-1]
			image_dst_path = os.path.join(save_dir, f"{i}.{image_ext}")

			if image is not None:
				# Download the image URL
				with open(image_dst_path, "wb") as fh:
					image.raw.decode_content = True

					try:
						shutil.copyfileobj(image.raw, fh)
					except:  # Catch everything and call it a day
						pass
					else:
						image_paths.append(image_dst_path)

		return image_paths

