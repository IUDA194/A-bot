import aspose.words as aw
from aspose.words.drawing import *
from PIL import Image, ImageDraw, ImageFont, ImageColor

fileNames = [ "passport.png", "img3.jpg" ]

class passport_gen:

    passport_path = "templates/passport.png"
    user_id = None
    photo_path = None
    name = None
    second_name = None
    father_name = None
    sex = None
    birthday = None
    passport_end_day = None
    regestratin_number = None
    document_number = None

    def __init__(self,
                    user_id : str,                 
                    photo_name : str,
                    name : str,
                    second_name : str, 
                    father_name : str,  
                    sex : str, 
                    birthday : str, 
                    passport_end_day : str, 
                    regestratin_number : str, 
                    document_number : str,
                    template_path) -> None:
        #self.gen_passport(photo_name, name, second_name, father_name,  sex, birthday, passport_end_day, regestratin_number, document_number)
        self.photo_path = photo_name
        self.user_id = user_id
        self.name = name
        self.second_name = second_name
        self.father_name = father_name
        self.sex = sex
        self.birthday = birthday
        self.passport_end_day = passport_end_day
        self.regestratin_number = regestratin_number
        self.document_number = document_number
        self.passport_path = template_path


    def gen_passport(self) -> dict:
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc)

        builder.insert_image(open(self.passport_path, "rb"),
            aw.drawing.RelativeHorizontalPosition.MARGIN,
            0,
            aw.drawing.RelativeVerticalPosition.MARGIN,
            0,
            1500,
            1000,
            aw.drawing.WrapType.SQUARE)

        builder.insert_image(open(self.photo_path, "rb"),
            aw.drawing.RelativeHorizontalPosition.MARGIN,
            100,
            aw.drawing.RelativeVerticalPosition.MARGIN,
            375,
            350,
            350,
            aw.drawing.WrapType.SQUARE)


        #builder.write(aw.ControlChar.TAB)
        #builder.insert_field("PAGE")
        #builder.insert_field("NUMPAGES")
        #builder.insert_html("<p>Hello<p>")


        # Вычислить максимальную ширину и высоту и обновить настройки страницы, 
        # чтобы обрезать документ по размеру изображений.
        pageSetup = builder.page_setup
        pageSetup.page_width = aw.ConvertUtil.pixel_to_point(2000)
        pageSetup.page_height = aw.ConvertUtil.pixel_to_point(1325)
        pageSetup.top_margin = aw.ConvertUtil.pixel_to_point(0)
        pageSetup.left_margin = aw.ConvertUtil.pixel_to_point(0)
        pageSetup.bottom_margin = aw.ConvertUtil.pixel_to_point(0)
        pageSetup.right_margin = aw.ConvertUtil.pixel_to_point(0)

        doc.save(f"{self.user_id}_r.jpg")

        self.insert_text(780, 370, self.second_name, 48)
        self.insert_text(780, 565, self.name, 48)
        self.insert_text(780, 725, self.father_name, 48)
        self.insert_text(780, 845, self.sex, 42)
        self.insert_text(785, 950, self.birthday, 42)
        self.insert_text(1320, 950, self.regestratin_number, 42)
        self.insert_text(785, 1065, self.passport_end_day, 42)
        self.insert_text(1320, 1065, self.document_number, 42)

        return f"{self.user_id}_r.jpg"

    def insert_text(self, x : int, y : int, text : str, font_size : int = 24):
        img = Image.open(f"{self.user_id}_r.jpg") 
        draw = ImageDraw.Draw(img)
        draw.text((x, y), text, fill="black", font=ImageFont.truetype("arial.ttf", font_size))
        img.save(f"{self.user_id}_r.jpg")
