'''
This script downloads the video from pexels when pexels video URL is passed

Usage: python main.py "{pexels_url}"
'''

from pexels_downloader import PexelsDownloader

if __name__ == "__main__":

    pexels_url = "https://www.pexels.com/video/waves-rushing-and-splashing-to-the-shore-1409899/"
    pexels_d = PexelsDownloader('logs/pexels_downloader.log')
    pexels_d.downloads_dir = "downloads/"
    pexels_d.resolution = 1080
    result = pexels_d.download(pexels_url)
    print(result)