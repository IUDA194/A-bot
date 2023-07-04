import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def check_facebook_user(users_id: str):
    result = []
    for user_id in list(map(str, users_id.split("\n"))):
        try:
            profile_url = f"https://www.facebook.com/{user_id}"

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
                            result.append(f"{user_id} 🔴 \n")
                        elif title_element and title_element.text == 'Увійти у Facebook':
                            print("title_element")
                            result.append(f"{user_id} 🟢 \n") #
                        elif soup.find('input', {'name': 'jazoest'}):
                            print(soup.find('input', {'name': 'jazoest'}))
                            result.append(f"{user_id} 🔴 \n")
                        else:
                            result.append(f"{user_id} 🟢 \n") #
                    else:
                        print("else")
                        result.append(f"{user_id} 🔴 \n")
        except aiohttp.ClientError:
            result.append(f"{user_id} 🔴 \n")
    return result

