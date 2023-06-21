import wget
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def tets():
    url = f'https://www.pizzabella.com.ua/'
    wget.download(url=url, out="sites.html")

tets()