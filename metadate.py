import io
from PIL import Image
import piexif

class photo_do:

    def __init__(self, p : str, u : str) -> None:
        self.photo_name = p
        self.user_id = u

    photo_name = ""
    user_id = ""

    def unik_photo(self) -> dict:
        o = io.BytesIO()
        print(self.photo_name)
        thumb_im = Image.open(f"{self.photo_name}.jpg")
        thumb_im.thumbnail((thumb_im.height, thumb_im.width), Image.ANTIALIAS)           
        thumb_im.save(o, "jpeg")
        thumbnail = o.getvalue()

        zeroth_ifd = {piexif.ImageIFD.Make: u"Canon",
                    piexif.ImageIFD.XResolution: (thumb_im.height, 1),
                    piexif.ImageIFD.YResolution: (thumb_im.width, 1),
                    piexif.ImageIFD.Software: u"piexif"
                    #piexif.ImageIFD.Compression: "int16u!",
                    }
        exif_ifd = {piexif.ExifIFD.DateTimeOriginal: u"2099:09:29 10:10:10",
                    piexif.ExifIFD.DateTimeDigitized: u"2099:09:29 10:10:10",
                    #piexif.ExifIFD.ApertureValue: rational64u,1.6959938128383605            # Вот это все нужно записать как разные числа в определенном 
                    #piexif.ExifIFD.BrightnessValue: 'rational64s',1.5728160952766375        # формате, тут записаны форматы, я смотрел на сайте который прикрепил
                    #piexif.ExifIFD.ColorSpace: 'int16u',65535                               # но как я понял это вообще к питону не относится, просто как число или стр
                    #piexif.ExifIFD.ComponentsConfiguration: 'undef[4]!',                    
                    #piexif.ExifIFD.ExifVersion: undef,0232
                    #piexif.ExifIFD.ExposureBiasValue: (0, 0),
                    piexif.ExifIFD.LensMake: u"LensMake",
                    piexif.ExifIFD.Sharpness: 65535,
                    piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
                    }
        gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
                piexif.GPSIFD.GPSAltitudeRef: 1,
                piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
                }
        first_ifd = {piexif.ImageIFD.Make: u"Canon",
                    piexif.ImageIFD.XResolution: (thumb_im.height, 1),
                    piexif.ImageIFD.YResolution: (thumb_im.width, 1),
                    piexif.ImageIFD.Software: u"piexif",
                    piexif.ImageIFD.DateTime: u"2099:09:29 10:10:10",
                    }

        exif_dict = {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd} #, "thumbnail":thumbnail}
        exif_bytes = piexif.dump(exif_dict)
        im = Image.open(f"{self.photo_name}.jpg")
        im.thumbnail((thumb_im.width, thumb_im.height), Image.ANTIALIAS)
        im.save(f"{self.user_id}_r.jpg", exif=exif_bytes)
        return {"status" : True, "result_path" : f"{self.user_id}_r.jpg" }