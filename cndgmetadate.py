from exif import Image

with open("img4.jpg", "rb") as palm_1_file:
    palm_1_image = Image(palm_1_file)
#with open("img3.jpg", "rb") as palm_2_file:
#    palm_2_image = Image(palm_2_file)


images = [ palm_1_image]

for index, image in enumerate(images):
    if image.has_exif:
        status = f"contains EXIF (version {image.exif_version}) information."
    else:
        status = "does not contain any EXIF information."
    print(image._has_exif)
    print(f"Image {index} {status}")
