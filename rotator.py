from id_detection import detect_objects
def rotate(image_path):
    detected_data = detect_objects(image_path)
    data = {}
    horizontal = False
    vertical = False

    person = False
    text = False
    logo = False
    all = False

    logo_coordinate = []
    person_coordinate = []
    text_coordinate = []
    all_coordinate = []

    orientation = ""
    for var in detected_data:
        data["text"] = var["class"]
        data["coordinate"] = var ["coordinate"]
        if(data["text"] == "text"):
            text = True
            text_coordinate = var ["coordinate"]
            width = data["coordinate"][1] - data["coordinate"][0]
            height = data["coordinate"][3] - data["coordinate"][2]
            if(width > height):
                horizontal = True
            else:
                vertical = True
        if(data["text"] == "logo"):
            logo = True
            logo_coordinate = var["coordinate"]
        if(data["text"] == "person"):
            person = True
            person_coordinate = var["coordinate"]
            width = data["coordinate"][1] - data["coordinate"][0]
            height = data["coordinate"][3] - data["coordinate"][2]
            if(width < height):
                horizontal = True
            else:
                vertical = True
        if(data["text"] == "all"):
            all = True
            all_coordinate = var["coordinate"]
            width = data["coordinate"][1] - data["coordinate"][0]
            height = data["coordinate"][3] - data["coordinate"][2]
            if(width > height):
                horizontal = True
            else:
                vertical = True
    if(horizontal):
        if(logo == True and person == True):
            if(logo_coordinate[2] < person_coordinate[2]):
                orientation = "true"
            else:
                orientation = "flip_180"
        elif(logo == True and text == True):
            if(logo_coordinate[2] < text_coordinate[2]):
                orientation = "true"
            else:
                orientation = "flip_180"
        elif(person == True and text == True):
            if(text_coordinate[2] < person_coordinate[2]):
                orientation = "true"
            else:
                orientation = "flip_180"
        elif(all == True):
            if(logo == True):
                if(all_coordinate[2] - logo_coordinate[2] < all_coordinate[3] - logo_coordinate[3]):
                    orientation = "true"
                else:
                    orientation = "flip_180"
            elif(person == True):
                if(all_coordinate[2] - person_coordinate[2] > all_coordinate[3] - person_coordinate[3]):
                    orientation = "true"
                else:
                    orientation = "flip_180"
            elif(text == True):
                if(all_coordinate[2] - text_coordinate[2] < all_coordinate[3] - text_coordinate[3]):
                    orientation = "true"
                else:
                    orientation = "flip_180"
            else:
                orientation = "img_error"
        else:
            orientation = "img_error"
    elif(vertical):
        if(logo == True and person == True):
            if(logo_coordinate[0] < person_coordinate[0]):
                orientation = "rorate_90"
            else:
                orientation = "rorate_270"
        elif(logo == True and text == True):
            if(logo_coordinate[0] < text_coordinate[0]):
                orientation = "rorate_90"
            else:
                orientation = "rorate_270"
        elif(person == True and text == True):
            if(text_coordinate[0] < person_coordinate[0]):
                orientation = "rorate_90"
            else:
                orientation = "rorate_270"
        elif(all == True):
            if (logo == True):
                if (all_coordinate[0] - logo_coordinate[0] < all_coordinate[1] - logo_coordinate[1]):
                    orientation = "rorate_90"
                else:
                    orientation = "rorate_270"
            elif (person == True):
                if (all_coordinate[0] - person_coordinate[0] > all_coordinate[1] - person_coordinate[1]):
                    orientation = "rorate_90"
                else:
                    orientation = "rorate_270"
            elif (text == True):
                if (all_coordinate[0] - text_coordinate[0] < all_coordinate[1] - text_coordinate[1]):
                    orientation = "rorate_90"
                else:
                    orientation = "rorate_270"
            else:
                orientation = "img_error"
        else:
            orientation = "img_error"
    else:
        orientation = "img_error"

    if(all == True and text == False):
        return orientation, all_coordinate, None
    elif(all == True and text == True):
        return orientation, all_coordinate, text_coordinate
    else:
        return orientation, None, None
