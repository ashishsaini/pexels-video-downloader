'''
This script downloads the video from pexels when pexels video URL is passed

Usage: python main.py "{pexels_url}"
'''

from pexels_downloader import PexelsDownloader

if __name__ == "__main__":

    # downlaod video
    # pexels_url = "https://www.pexels.com/video/waves-rushing-and-splashing-to-the-shore-1409899/"
    # pexels_d = PexelsDownloader('logs/pexels_downloader.log')
    # video_id = pexels_d.get_id_from_url(pexels_url)
    # pexels_d.downloads_dir = "downloads/"
    # pexels_d.resolution = 1080
    # result = pexels_d.download(video_id)
    # print(result)

    #exit()

    # search video
    pexels_d = PexelsDownloader('logs/pexels_downloader.log')
    pexels_d.downloads_dir = "downloads/"
    pexels_d.resolution = 1080
    result = pexels_d.search_video("forest")
    print(result)