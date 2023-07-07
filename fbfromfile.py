import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fb_from_file(file_name):
    with open(file_name, "r", encoding="utf8") as file:
        text = file.read()


    def extract_links(text):
        # Шаблон для поиска ссылок
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        # Используем функцию findall модуля re для поиска всех совпадений
        links = re.findall(pattern, text)
        return links

    links = extract_links(text)

    result = []
    active_akk = []
    deactive_akk = []
    active_number = 0
    deactive_number = 0
    for link in links:
        try:
            profile_url = link

            async with aiohttp.ClientSession() as session:
                async with session.get(profile_url) as response:
                    print(response.status)
                    if response.status == 200:
                        content = await response.text()
                        soup = BeautifulSoup(content, 'html.parser')
                        title_element = soup.find('title')
                        print(title_element)
                        if title_element and title_element.text == 'Facebook':
                            print("title_element")
                            result.append(f"{link} Не доступен \n")
                            deactive_akk.append(f"{link} Не доступен \n")
                            deactive_number += 1
                        elif title_element and title_element.text == 'Увійти у Facebook':
                            print("title_element")
                            result.append(f"{link} Доступен \n") #
                            active_akk.append(f"{link} Доступен \n")
                            active_number += 1
                        elif soup.find('input', {'name': 'jazoest'}):
                                print(soup.find('input', {'name': 'jazoest'}))
                                result.append(f"{link} Не доступен \n")
                                deactive_akk.append(f"{link} Не доступен \n")
                                deactive_number += 1
                        else:
                                result.append(f"{link} Доступен \n") #
                                active_akk.append(f"{link} Доступен \n")
                                active_number += 1
                    else:
                            print("else")
                            result.append(f"{link} Не доступен \n")
                            deactive_akk.append(f"{link} Не доступен \n")
                            deactive_number += 1
        except aiohttp.ClientError:
                result.append(f"{link} Не доступен \n")
    return {"result" : result, "active_number" : active_number, "deactive_number" : deactive_number, "active_akk" : active_akk, "deactive_akk" : deactive_akk}