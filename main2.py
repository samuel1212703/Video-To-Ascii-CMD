# Video to ASCII Art
# Created on 16 may 2025
# Author: samuel1212703
# Based on a program by: jsimb
# Transforms a video of any format into ascii art. The ascii art is displayed in the cmd window.
# Tested with python3.12

from PIL import Image
import cv2
import os
import msvcrt
import time

# You can experiment with custom charsets for styling you ascii video
charset = list("QRVILr:'.- ")  # 11 tonal ranges of 24 pixels each
# charset = list(" -.':rLIVXRMWQ@") #15 tonal ranges of 18 pixels each
# charset = list("@&B9#SGHMh352AXsri;:~,. ") #24 tonal ranges of ~11 pixels each

f = "test.mp4"
fps = 60
max_height = 30  # Height of ASCII output in rows
char_ratio = 1.65  # Width-to-height ratio of terminal font
os.system("mode con: cols=200 lines={}".format(max_height))


# Load video with cv2
vidcap = cv2.VideoCapture(f)


def generateAscii():
    # Try to get cv2 image array
    success, frame = vidcap.read()
    if not success or frame is None:
        return False

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR to RGB
    color_img = Image.fromarray(frame_rgb)  # from cv2 array
    img = color_img.convert("L")  # to greyscale

    # Resize image
    w, h = img.size
    new_w = int(w / h * max_height * char_ratio)
    img = img.resize((new_w, max_height), Image.LANCZOS)

    # Image to ascii text
    pixels = img.getdata()
    shades = len(charset)
    ascii_str = ""
    for i, lum in enumerate(pixels):
        if i % new_w == 0 and i != 0:
            ascii_str += "\n"
        index = (255 - lum) * shades // 256
        ascii_str += charset[min(index, shades - 1)]

    print(ascii_str)
    time.sleep(1 / fps)
    return True


while generateAscii():
    if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():  # Escape
        break  # Stop on keypress

# os.system("cls")  # clear console
