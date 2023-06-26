import pyotp

class twofa:
    def gen_code(key : str):
        # Тестовый ключ 2FA для разработки и отладки
        test_key = key

        # Создайте объект TOTP с использованием тестового ключа
        totp = pyotp.TOTP(test_key)

        # Сгенерируйте 2FA-код
        code = totp.now()

        return code

