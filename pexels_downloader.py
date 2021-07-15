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


class PexelsDownloader:

    def __init__(self) -> None:
        self.resolution = 1080
        self.pexels_api_url = "https://api.pexels.com/videos/videos/"
        self.pexels_api_key = os.environ.get("PEXELS_API_KEY")
        self.timeout = 30
        self.max_resolution = 1440
        self.downloads_dir = "/tmp/"
        self.trace_id = str(uuid.uuid4())
        self.log_path = 'logs/pexels_downloader.log'
        logging.basicConfig(filename=self.log_path,format=f'%(asctime)s | %(levelname)s | {self.trace_id} | %(message)s', level=logging.INFO)


    def _check_env(self, key):
        # check if required environment variable is set
        if not os.environ.get(key):
            return False
        
        return True

    def _get_video_by_id(self, id):
        url = f"{self.pexels_api_url}{id}"
        headers = {"Authorization": self.pexels_api_key}
        try:
            result = requests.get(url, headers=headers, timeout=self.timeout)
        except Exception as e:
            logging.warning(f"Error: unable to get video from video id")
            logging.error(f"{e}")
            exit()
        return result.text


    def _check_and_create_dir(self, dir):
        if not os.path.exists(dir):
            try:
                os.mkdir(dir)
            except Exception as e:
                logging.warning(f"Unable to create required downloads directory: {dir}")
                logging.error(f"{e}")
                exit()
        return True

    def _download_video(self, video_url, downloads_dir, filename):
        self._check_and_create_dir(downloads_dir)
        try:
            r = requests.get(video_url, allow_redirects=True, timeout=self.timeout)
        except Exception as e:
            logging.warning(f"Error: Unable to download video : {video_url}")
            logging.error(f"{e}")
            exit()
        
        open(os.path.join(downloads_dir, filename), 'wb').write(r.content)

        return os.path.join(downloads_dir, filename)

    def _select_video(self, video_data, req_resolution):
        # selects required resolution from various available resolutions
        if "video_files" not in video_data:
            logging.error(f"Error: Unexpected response when getting data from: {video_data}")
            exit()

        selected_video = {}
        highest_res = 0
        highest_res_selected = {}
        for video in video_data['video_files']:
            if video['height'] == req_resolution and "mp4" in video['file_type']:
                selected_video = video

            if video['height'] is not None and video['height'] > highest_res and "mp4" in video['file_type'] and video['height'] <= self.max_resolution:
                highest_res = video['height']
                highest_res_selected = video

        if not selected_video:
            # if no video with required resolution, then download highest resolution
            selected_video = highest_res_selected

        return selected_video


    def _get_id_from_url(self, pexels_url):
        id = pexels_url.split("-")[-1].replace("/", "")
        
        if len(id) < 3 or len(id) > 10:
            logging.error(f"rror: unable to get valid id from url {pexels_url}")
            exit()
        return id


    def _run(self, id):
        try:
            video_data = json.loads(self._get_video_by_id(id))
        except Exception as e:
            logging.warning(f"Error: returned video data not in json format")
            logging.error(f"{e}")
            exit()

        logging.info(f"{self.trace_id} | got response from pexels : "+json.dumps(video_data))    
        
        selected_video = self._select_video(video_data, self.resolution)
        logging.info(f"{self.trace_id} | selected video : "+json.dumps(selected_video))    

        if not selected_video:
            logging.info(f"{video_data}")
            logging.error(f"Unable to get required file, some error")
            exit()

        filename = str(uuid.uuid4())+".mp4"
        video_path = self._download_video(selected_video['link'], self.downloads_dir, filename)

        filesize = str(os.path.getsize(video_path))
        logging.info(f"Downloaded file size : {filesize}") 

        return video_path


    def download(self, pexels_url):
        # public function, to be called from
        if not self._check_env("PEXELS_API_KEY"):
            logging.error(f"Error: required Pexels API key is not set in environment variable")
            exit()

        logging.info(f"{self.trace_id} | got url: {pexels_url}")
        id = self._get_id_from_url(pexels_url)
        return self._run(id)
