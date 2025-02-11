from PIL import Image

import os

def remove_image_metadata():
    for root, dirs, files in os.walk("root/assets/images"):
        path = root.split(os.sep)
        for file in files:
            end = file[-4:].lower()
            if end == ".jpg" or end == ".png":
                remove_data(path, file)

def remove_data(path, file):
    file_name = os.path.join(*path, file)
    image = Image.open(file_name)
        
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
        
    image_without_exif.save(file_name)
    
    image_without_exif.close()
    print("Fixed file", file_name)


