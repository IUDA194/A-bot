import requests

def gen_photo(user_id : str):
    p = requests.get("https://thispersondoesnotexist.com/")
    out = open(f"{user_id}.jpg", "wb")
    out.write(p.content)
    out.close()