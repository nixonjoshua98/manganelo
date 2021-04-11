import os
import shutil
import tempfile
import typing
import dataclasses

import functools as ft

from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup
from PIL import Image

from manganelo.api.apibase import APIBase
from manganelo.api.chapterinfo import ChapterInfo


@dataclasses.dataclass
class ChapterStatus:
	title: str
	saved_ok: bool
	percent_saved: float
	path: str


class DownloadChapter(APIBase):
	def __init__(self, src_url: str, dst_path: str, *, threaded: bool = False):
		"""
		Object constructor

		:param src_url: The  chapter which we will be downloading
		:param dst_path: The path where the chapter will be saved after completion
		:param threaded: Whether the bulk of the work will be done on a seperate thread or the main thread
		"""

		self._src_url = src_url
		self._dst_path = self._update_destination_path(dst_path)
		self._title = None

		self._saved = False
		self._percent_saved = 0

		super(DownloadChapter, self).__init__(threaded)

	@ft.cached_property
	def results(self):
		"""
		Returns the status of the download.

		:return ChapterStatus: The status of the chapter
		"""

		self._join_thread()

		return ChapterStatus(
			saved_ok=self._saved,
			percent_saved=self._percent_saved,
			path=self._dst_path,
			title=self._title
		)

	def _start(self):
		""" The main function...Where the magic happens. """

		r = self.send_request(self._src_url)

		soup = BeautifulSoup(r.content, "html.parser")

		chap = ChapterInfo.from_soup(soup)

		self._title = chap.title

		with tempfile.TemporaryDirectory() as temp_dir:
			image_paths = self._download_images(chap.image_urls, temp_dir)

			num_pages = self._create_pdf(image_paths)

			self._percent_saved = num_pages / len(chap.image_urls)

	def _download_images(self, image_urls: typing.List[str], save_dir: str) -> typing.List[str]:
		"""
		Download images from a sequence of URLS into a directory.

		:param image_urls: List of URLS which we will attempt to download here
		:param save_dir: The directory where the downloaded images will be saved
		:return list: List of paths where the downloaded images are stored
		"""

		image_paths = []

		for i, url in enumerate(image_urls):
			image = self.send_request_image(url)

			image_ext = url.split(".")[-1]

			image_dst_path = os.path.join(save_dir, f"{i}.{image_ext}")

			if image is not None:
				with open(image_dst_path, "wb") as fh:

					# Magic boolean which makes it work
					image.raw.decode_content = True

					# noinspection PyBroadException

					# Attempt to download the image from the URL
					try:
						shutil.copyfileobj(image.raw, fh)

					# We should reduce the scope
					except Exception:
						pass

					# We downloaded the image without any errors
					else:
						image_paths.append(image_dst_path)

		return image_paths

	def _update_destination_path(self, path):
		""" Remove the illegal characters from the file path. """

		dir_, file = os.path.split(path)

		for char in ("\\", "/", ":", "*", "?", "<", ">", "|"):
			file = file.replace(char, " ")

		return os.path.join(dir_, file)

	def _create_pdf(self, images: typing.List[str]) -> int:
		"""

		:param images: List of image paths which we will attempt to convert into a PDF
		:return int: The number of pages in the PDF
		"""

		pdf = canvas.Canvas(self._dst_path)

		num_pages = 0

		for image in images:
			try:
				with Image.open(image) as img:
					w, h = img.size

			except (OSError, UnboundLocalError):
				continue

			# Set the page dimensions to the image dimensions
			pdf.setPageSize((w, h))

			try:
				# Insert the image onto the current page
				pdf.drawImage(image, x=0, y=0)

			except OSError:
				continue

			# Create a new page ready for the next image
			pdf.showPage()

			num_pages += 1

		if num_pages > 0:
			dirs = os.path.dirname(self._dst_path)

			# Create the path if it doesn't exist already
			if dirs:
				os.makedirs(dirs, exist_ok=True)

			try:
				pdf.save()
			except FileNotFoundError:
				pass

			else:
				self._saved = True

		return num_pages
