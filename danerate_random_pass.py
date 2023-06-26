import random

class random_password:

    CHARS_LVL_1 = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    CHARS_LVL_2 = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    CHARS_LVL_3 = 'abcdefghijklnopqrstuvwxyz1234567890'

    PASSWORD = None

    def __init__(self,lvl : int = 1, lenth : int = 8, number : int = 1) -> None:
        self.PASSWORD = self.genarate_rand_pass(lvl, lenth, number)
    
    def genarate_rand_pass(self,lvl : int = 1, lenth : int = 8, number : int = 1) -> dict:
        if lvl == 1: chars = self.CHARS_LVL_1
        if lvl == 2: chars = self.CHARS_LVL_2
        if lvl == 3: chars = self.CHARS_LVL_3
        else: return {"status" : False, "error" : f"Incorrect input lvl! You can enter 1, 2, or 3. Your input is {lvl}"}
        if type(lenth) != int:
            return {"status" : False, "error" : f"Incorrect input len! You can enter integer type. Your input have type: {type(len)}"}
        if type(number) == int:
            if number <= 0:
                return {"status" : False, "error" : f"Incorrect input number! You can enter positive integer type. Your input is: {number}"}
        else:
            return {"status" : False, "error" : f"Incorrect input number! You can enter positive integer type. Your input have type: {type(number)}"}
        result = []
        result_text = ""
        temp_pass = ""
        for i in range(number):
            for i in range(lenth):
                temp_pass += chars[random.randint(0, len(chars) - 1)]
            result.append(temp_pass)
            result_text += temp_pass + "\n"
            temp_pass = ""
        return {"status" : True, "result" : result, "text" : result_text}
