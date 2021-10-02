'''
This script downloads the video from pexels when pexels video URL is passed

Usage: python main.py "{pexels_url}"
'''


from genericpath import exists
import json
import requests
import os
import uuid
import logging
import random


class ImageDownloader:

    def __init__(self, log_path="pexels_downloader.log") -> None:
        self.resolution_width = 1920
        self.resolution_height = 1080
        self.pexels_api_url = "https://api.pexels.com/v1/"
        self.pexels_api_key = os.environ.get("PEXELS_API_KEY")
        self.timeout = 30
        self.max_resolution = 1440
        self.downloads_dir = "/tmp/"
        self.trace_id = str(uuid.uuid4())
        self.log_path = log_path
        logging.basicConfig(
            filename=self.log_path, format=f'%(asctime)s | %(levelname)s | {self.trace_id} | %(message)s', level=logging.INFO)

    def _check_env(self, key):
        # check if required environment variable is set
        if not os.environ.get(key):
            return False

        return True

    def get_image(self, keyword):
        # Public endpoint to search the video
        search_result_raw = self._image_search_request(keyword)

        try:
            search_result = json.loads(search_result_raw)
        except Exception as e:
            logging.warning(f"Error: Unable to search video : {keyword}")
            logging.error(f"{e}")
            exit()

        if "photos" not in search_result or len(search_result['photos']) < 1:
            return False

        index = random.randint(0, len(search_result['photos'])-1)

        selected_image = f""+search_result['photos'][index]["src"]["original"] + \
            "?auto=compress&cs=tinysrgb&fit=crop&h=" + \
            str(self.resolution_height)+"&w="+str(self.resolution_width)

        return selected_image

    def _image_search_request(self, keyword):
        # request the pexels APi for video
        url = f"{self.pexels_api_url}search/?query={keyword}&per_page=20&orientation=landscape"
        headers = {"Authorization": self.pexels_api_key}

        try:
            result = requests.get(url, headers=headers, timeout=self.timeout)
        except Exception as e:
            logging.warning(f"Error: unable to get video from video id")
            logging.error(f"{e}")
            exit()
        return result.text
