import requests
import os
from urllib.parse import urlparse, urljoin
import re
import shutil
import urllib.parse
from bs4 import BeautifulSoup
import io
import zipfile

class dowonload_site:
    
    name = None
    url = None
    output_dir = "sites"
    zip_path = None
    
    def __init__(self, name : str, url : str) -> None:
        self.name = name
        self.url = url
        self.download_files()
        self.zip_path = self.gen_zip()
    
    def download_files(self):
        response = requests.get(self.url)
        try:
            os.mkdir(os.path.abspath(f"sites/{self.name}"))
            os.rmdir(os.path.abspath(f"sites/{self.name}"))
            os.mkdir(os.path.abspath(f"sites/{self.name}"))
        except:
            shutil.rmtree(os.path.abspath(f"sites/{self.name}"))
            os.mkdir(os.path.abspath(f"sites/{self.name}"))
        if response.status_code == 200:
            # Создаем каталог для сохранения файлов
            parsed_url = urlparse(self.url)
            domain = parsed_url.netloc
            os.makedirs(domain, exist_ok=True)

            # Сохраняем файлы CSS и JS
            for file_url in self.extract_file_urls(response.text, domain, parsed_url.scheme):
                filename = os.path.basename(file_url)
                file_path = os.path.join(f"sites/{self.name}", urllib.parse.quote(filename))  # Преобразуем имя файла
                file_response = requests.get(file_url)
                if file_response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(file_response.content)
                    print(f'Successfully downloaded: {file_path}')
                else:
                    print(f'Failed to download: {file_url}')

            # Парсим HTML и сохраняем страницу с примененными стилями
            soup = BeautifulSoup(response.text, 'html.parser', from_encoding="utf-8")
            css_files = soup.find_all('link', rel='stylesheet')
            for css_file in css_files:
                css_url = css_file['href']
                if not css_url.startswith('http'):
                    css_url = urljoin(self.url, css_url)
                css_response = requests.get(css_url)
                if css_response.status_code == 200:
                    css_filename = os.path.basename(css_url)
                    css_filename = urllib.parse.quote(css_filename)  # Преобразуем имя файла
                    css_path = os.path.join(f"sites/{self.name}", css_filename)
                    with open(css_path, 'wb') as file:
                        file.write(css_response.content)
                    css_file['href'] = css_filename
                    print(f'Successfully downloaded and updated CSS: {css_path}')
                else:
                    print(f'Failed to download CSS: {css_url}')

            html_filename = os.path.join(f"sites/{self.name}", 'index.html')
            with io.open(html_filename, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
            print(f'Successfully downloaded and updated HTML: {html_filename}')
        else:
            print(f'Failed to access URL: {self.url}')

    def extract_file_urls(self, html, domain, scheme):
        # Извлекаем URL-адреса файлов CSS и JS из HTML
        # Преобразуем относительные URL-адреса в абсолютные

        pattern = r'(?:href|src)="([^"]+\.(?:css|js))"'
        relative_urls = re.findall(pattern, html)

        absolute_urls = []
        for relative_url in relative_urls:
            absolute_url = urljoin(f'{scheme}://{domain}', relative_url)
            absolute_urls.append(absolute_url)

        return absolute_urls

    def gen_zip(self):
        with zipfile.ZipFile(f"sites/{self.name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(f"sites/{self.name}"):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.output_dir))
        self.zip_path = f"sites/{self.name}.zip"
        return f"sites/{self.name}.zip"
