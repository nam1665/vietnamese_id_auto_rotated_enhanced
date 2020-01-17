from rotator import rotate
from PIL import Image
import os


def imgage_crop_enhanced(image_path_detect):
    result = rotate(image_path_detect)
    img = Image.open(image_path_detect)
    name = os.path.basename(image_path_detect)
    rotated_folder = './rotated/'
    all_folder = './cut_all/'
    text_folder = './text/'
    if(result[0] == "true"):
        if(result[1] is not None):
            if not os.path.exists(all_folder):
                os.makedirs(all_folder)
            region = img.crop((result[1][0],result[1][2], result[1][1], result[1][3] ))
            region.save(all_folder + name.split('.')[0] + "_all.jpg")
        if(result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = img.crop((result[2][0],result[2][2], result[2][1], result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_text.jpg")
    elif(result[0] == "flip_180"):
        if not os.path.exists(rotated_folder):
            os.makedirs(rotated_folder)
        transposed = img.transpose(Image.ROTATE_180)
        flip_path = rotated_folder + name.split('.')[0] + "_rotated_180.jpg"
        transposed.save(flip_path)
        flip_result = rotate(flip_path)
        flip_img = Image.open(flip_path)
        if(flip_result[1] is not None):
            if not os.path.exists(all_folder):
                os.makedirs(all_folder)
            region = flip_img.crop((flip_result[1][0],flip_result[1][2], flip_result[1][1], flip_result[1][3] ))
            region.save(all_folder + name.split('.')[0] + "_rotated_180_all.jpg")
        if(flip_result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = flip_img.crop((flip_result[2][0],flip_result[2][2], flip_result[2][1], flip_result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_rotated_180_text.jpg")
    elif(result[0] == "rorate_90"):
        if not os.path.exists(rotated_folder):
            os.makedirs(rotated_folder)
        transposed = img.transpose(Image.ROTATE_270)
        flip_path = rotated_folder + name.split('.')[0] + "_rotated_90.jpg"
        transposed.save(flip_path)
        flip_result = rotate(flip_path)
        flip_img = Image.open(flip_path)
        if(flip_result[1] is not None):
            if not os.path.exists(all_folder):
                os.makedirs(all_folder)
            region = flip_img.crop((flip_result[1][0],flip_result[1][2], flip_result[1][1], flip_result[1][3] ))
            region.save(all_folder + name.split('.')[0] + "_rotated_90_all.jpg")
        if(flip_result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = flip_img.crop((flip_result[2][0],flip_result[2][2], flip_result[2][1], flip_result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_rotated_90_text.jpg")
    elif(result[0] == "rorate_270"):
        if not os.path.exists(rotated_folder):
            os.makedirs(rotated_folder)
        transposed = img.transpose(Image.ROTATE_90)
        flip_path = rotated_folder + name.split('.')[0] + "_rotated_270.jpg"
        transposed.save(flip_path)
        flip_result = rotate(flip_path)
        flip_img = Image.open(flip_path)
        if(flip_result[1] is not None):
            if not os.path.exists(all_folder):
                os.makedirs(all_folder)
            region = flip_img.crop((flip_result[1][0],flip_result[1][2], flip_result[1][1], flip_result[1][3] ))
            region.save(all_folder + name.split('.')[0] + "_rotated_270_all.jpg")
        if(flip_result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = flip_img.crop((flip_result[2][0],flip_result[2][2], flip_result[2][1], flip_result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_rotated_270_text.jpg")

        return "ok"

    else:
        return "img_error"


image_path_detect = 'test.jpg'
imgage_crop_enhanced(image_path_detect)