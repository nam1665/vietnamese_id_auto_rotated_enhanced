from rotator import rotate
from PIL import Image
import os
import cv2

# Automatic brightness and contrast optimization with optional histogram clipping
def automatic_brightness_and_contrast(image, clip_hist_percent=25):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/180.0)
    clip_hist_percent /= 4

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)


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
            crop_img = cv2.imread(all_folder + name.split('.')[0] + "_all.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(all_folder + name.split('.')[0] + "_all.jpg", auto_result)

        if(result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = img.crop((result[2][0],result[2][2], result[2][1], result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_text.jpg")
            crop_img = cv2.imread(text_folder + name.split('.')[0] + "_text.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(text_folder + name.split('.')[0] + "_text.jpg", auto_result)

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
            crop_img = cv2.imread(all_folder + name.split('.')[0] + "_rotated_180_all.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(all_folder + name.split('.')[0] + "_rotated_180_all.jpg", auto_result)
        if(flip_result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = flip_img.crop((flip_result[2][0],flip_result[2][2], flip_result[2][1], flip_result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_rotated_180_text.jpg")
            crop_img = cv2.imread(text_folder + name.split('.')[0] + "_rotated_180_text.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(text_folder + name.split('.')[0] + "_rotated_180_text.jpg", auto_result)
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
            crop_img = cv2.imread(all_folder + name.split('.')[0] + "_rotated_90_all.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(all_folder + name.split('.')[0] + "_rotated_90_all.jpg", auto_result)
        if(flip_result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = flip_img.crop((flip_result[2][0],flip_result[2][2], flip_result[2][1], flip_result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_rotated_90_text.jpg")
            crop_img = cv2.imread(text_folder + name.split('.')[0] + "_rotated_90_text.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(text_folder + name.split('.')[0] + "_rotated_90_text.jpg", auto_result)
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
            crop_img = cv2.imread(all_folder + name.split('.')[0] + "_rotated_270_all.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(all_folder + name.split('.')[0] + "_rotated_270_all.jpg", auto_result)
        if(flip_result[2] is not None):
            if not os.path.exists(text_folder):
                os.makedirs(text_folder)
            region = flip_img.crop((flip_result[2][0],flip_result[2][2], flip_result[2][1], flip_result[2][3] ))
            region.save(text_folder + name.split('.')[0] + "_rotated_270_text.jpg")
            crop_img = cv2.imread(text_folder + name.split('.')[0] + "_rotated_270_text.jpg")
            auto_result, alpha, beta = automatic_brightness_and_contrast(crop_img)
            cv2.imwrite(text_folder + name.split('.')[0] + "_rotated_270_text.jpg", auto_result)

        return "ok"

    else:
        return "img_error"


image_path_detect = 'test.jpg'
a = imgage_crop_enhanced(image_path_detect)
print(a)