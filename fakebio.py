from faker import Faker
from russian_names import RussianNames
import transliterate

class fake:
    name = None 
    adress = None

    def __init__(self, lang : str = "ru") -> None:
        self.name = self.gen_rand_name(lang)
        self.adress = self.gen_rand_adress(lang)

    # Генератор рандомных имён
    def gen_rand_name(self, lang : str = "ru") -> str:
        name = Faker(lang).name()
        return name
    
    # Генератор рандомных адресов
    def gen_rand_adress(self, lang : str = "ru") -> str:
        adress = Faker(lang).address()
        return adress

def gen_man_name():
    return RussianNames(gender=1).get_person()
    
def gen_girl_name():
    return RussianNames(gender=0).get_person()

def gen_girl_name_en():
    return transliterate.translit(RussianNames(gender=0).get_person(), reversed=True)

def gen_man_name_en():
    return transliterate.translit(RussianNames(gender=1).get_person(), reversed=True)
