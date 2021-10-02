'''
This script downloads the video from pexels when pexels video URL is passed

Usage: python main.py "{pexels_url}"
'''

from video_downloader import VideoDownloader
from image_downloader import ImageDownloader

if __name__ == "__main__":

    # search video
    video = VideoDownloader('logs/pexels_downloader.log')
    video.downloads_dir = "downloads/"
    video.resolution_width = 1080
    result = video.search_video("forest")
    print(result)

    # image search 
    image = ImageDownloader('logs/pexels_downloader.log')
    image.resolution_width = 1280
    image.resolution_height = 720
    result = image.get_image("black")
    print(result)
