import requests
import youtube_dl
from bs4 import BeautifulSoup

class Downloader:
    @staticmethod
    def get_parser(url):
        target = requests.get(url).content
        soup = BeautifulSoup(target, 'html.parser')
        ## mengambil nilai dari atribut "src" pada tag "script"
        src = soup.find('script', {'src': True})['src']

        # mengambil bagian kode video dari URL
        video_code = src.split('/')[-1].split('.')[0]
        return video_code
    
    @staticmethod
    def download(url):
        video_id = Downloader.get_parser(url)
        link_statik = f"https://fast.wistia.net/embed/iframe/{video_id}"
        
        ydl_opts = {           
            'format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link_statik])






