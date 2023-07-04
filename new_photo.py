from PIL import Image, ImageEnhance
import os
import shutil
import zipfile
import random

class new_photo_unik:

    # Параметры изменения
    brightness = 0.98
    contrast = 1.1
    sharpness = 1.1
    saturation = 1.1
    scale = 0.99
    resize = 0.98
    
    path_list = []

    user_id = None
    last_n_index = None
    zip_path = None

    # Путь к исходному изображению
    input_image = None

    # Папка для сохранения измененных изображений
    output_dir = "media"

    def __init__(self, image_path, id, i) -> None:
        self.input_image = image_path
        self.output_dir = f"media/{id}"
        self.user_id = id

        try:
            os.mkdir(os.path.abspath(f"media/{id}"))
        except:
            try:
                os.rmdir(os.path.abspath(f"media/{id}"))
                os.mkdir(os.path.abspath(f"media/{id}"))
            except:
                shutil.rmtree(os.path.abspath(f"media/{id}"))
                os.mkdir(os.path.abspath(f"media/{id}"))

        # Изменение изображения и сохранение 10 разных фото
        self.path_list = []
        for i in range(i):
            modified_image = self.modify_image(self.input_image,
                                               self.brightness, 
                                               self.contrast, 
                                               self.sharpness, 
                                               self.saturation, 
                                               self.scale, 
                                               self.resize, 
                                               self.output_dir, i)
            self.path_list.append(modified_image)
            print(f"Создано измененное изображение: {modified_image}")
        self.gen_zip()

    def gen_zip(self):
        with zipfile.ZipFile(f"media/{self.user_id}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.output_dir))
        self.zip_path = f"media/{self.user_id}.zip"
        return f"{self.user_id}.zip"

    def modify_image(self ,image_path, brightness, contrast, sharpness, saturation, scale, resize, output_dir, i):
        n_index = random.randrange(1, 3) / 100
        def n_c(n_index):
            if n_index == self.last_n_index:
                n_index = random.randrange(1, 3) / 100
                n_c(n_index)
            else: pass
        # Открытие изображения
        image = Image.open(image_path)

        # Изменение яркости
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness + n_index)

        # Изменение контрастности
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast + n_index)

        # Изменение резкости
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness + n_index)

        # Изменение насыщенности
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(saturation + n_index)

        # Изменение масштаба
        width, height = image.size
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height))

        # Изменение ширины и высоты
        width_change = int(width * resize)
        height_change = int(height * resize)
        new_width = width + width_change
        new_height = height + height_change
        image = image.resize((new_width, new_height))

        # Удаление EXIF-данных
        image = image.convert("RGB")
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)

        # Генерация имени нового файла
        filename = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_dir, f"{random.randint(1, 10000000)}.png")

        # Генерация имени нового файла
        filename = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_dir, f"{random.randint(1, 10000000)}.png")

        # Сохранение измененного изображения
        image_without_exif.save(output_path, "PNG")

        return output_path
