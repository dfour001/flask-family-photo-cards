from PIL import Image, ImageDraw, ImageFont
from PIL.ImageOps import exif_transpose
from PIL.ImageColor import getrgb

import os
from math import floor



inputFont = r'C:\Users\danie\AppData\Local\Microsoft\Windows\Fonts\Oswald-VariableFont_wght.ttf'


def get_font(fontPath, text, fontSize=120, maxWidth=1200):
    maxWidth = maxWidth - 48  # Ensure minimum 24px margin
    font = ImageFont.truetype(fontPath, fontSize)
    
    while font.getlength(text) > maxWidth:
        fontSize -= 3
        font = ImageFont.truetype(fontPath, fontSize)

    return font


def get_orientation(image):
    """ Determines and returns image orientation based on width and height measurements """
    width, height = image.size

    if width > height:
        orientation = 'landscape'
    elif height > width:
        orientation = 'portrait'
    else:
        orientation = 'square'
    
    return orientation


def create_card(portrait, text, outputPath, fontPath=inputFont, size=(1200,1800), cardColor='#FFFFFF', textColor='#000000', autoCrop=True, uncroppedColor='#FFFFFF'):

    # Create output card image
    outputImg = Image.new(mode="RGB", size=size, color=cardColor)

    # Load input portrait
    loadPortrait = Image.open(portrait)
    loadPortrait = exif_transpose(loadPortrait) # Rotate image if needed

    # Scale input portrait and put in place
    if autoCrop:
        imgOrientation = get_orientation(loadPortrait)
        imgWidth, imgHeight = loadPortrait.size
        
        # Determine cropping box
        x1 = 0 if imgOrientation == 'portrait' else (imgWidth - imgHeight) / 2
        y1 = 0 if imgOrientation == 'landscape' else (imgHeight/2) - (imgWidth/2)
        x2 = imgWidth - x1
        y2 = imgHeight - y1
        cropBox = (x1, y1, x2, y2)

        # Crop
        loadPortrait = loadPortrait.crop(cropBox)
        
    else:
        # Create the background color for images that do not fill the full space
        uncroppedBackground = Image.new(mode="RGB", size=(size[0], size[0]), color=uncroppedColor)
        outputImg.paste(uncroppedBackground)

    # Shrink input image to fit card
    loadPortrait.thumbnail((size[0], size[0]))
    
    # Determine paste box
    imgWidth, imgHeight = loadPortrait.size
    x1 = floor((size[0]/2) - (imgWidth/2))
    y1 = floor((size[0]/2) - (imgHeight/2))
    x2 = imgWidth + x1
    y2 = imgHeight + y1

    box = (x1, y1, x2, y2)
    outputImg.paste(loadPortrait, box)

    # Calculate text location
    portraitHeight = size[0] # portraitHeight == cardWidth, since the image section is 1200px x 1200px
    cardHeight = size[1]
    textY = (cardHeight - portraitHeight) / 2 + portraitHeight
    textX = portraitHeight / 2

    # Enter text
    draw = ImageDraw.Draw(outputImg)
    draw.text((textX,textY), text, fill=textColor, anchor='mm', font=get_font(fontPath, text, maxWidth=size[0]))

    outputImg.save(outputPath)

    return outputImg


def get_input_images(path):
    fileNames = [file for file in os.listdir(path) if file.lower().endswith(('jpg', 'png'))]
    fileTexts = [file.split('.')[0].replace('_',' ') for file in fileNames]

    return list(zip(fileNames, fileTexts))


def get_unique_name(filename, files):
    """Creates a unique file name by adding a number to the beginning. If the first part is already a number,
    it will add 1 to that number.

    Args:
        filename (str): The current name of the file.
        files (list): The list of files in the user's folder created via os.listdir.

    Returns:
        str: A new unique file name.
    """
    filename_split = filename.split('_')
    num = None

    while True:
        if filename_split[0].isnumeric():
            num = int(filename_split[0])
            filename_split[0] = f'{int(filename_split[0]) + 1}'
        else:
            num = 1
            filename_split = [str(num), filename]
        
        new_filename = '_'.join(filename_split)
        
        if new_filename not in files:
            return new_filename
        
        num += 1

        
if __name__ == '__main__':
    print(get_unique_name('something_something.jpg', ['1_nadia.jpg', '2_nadia.jpg', '3_nadia.jpg', '4_nadia.jpg']))