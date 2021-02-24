# Image to ASCII Art
# Created on 7 Jul 2015
# Author: jsimb
#
# Writes a .txt file containing ascii art corresponding to an arbitrary image.
# Tested with python3.

from PIL import Image
import sys
import cv2
import os
import msvcrt

###############################################################

input1 = input("continously (y/n)? ")
input2 = input("file backup (y/n)? ")

greyscale = list("QRVILr:'.- ") #11 tonal ranges of 24 pixels each
#greyscale = list(" -.':rLIVXRMWQ@") #15 tonal ranges of 18 pixels each
#greyscale = list("@&B9#SGHMh352AXsri;:~,. ") #24 tonal ranges of ~11 pixels each

if len(sys.argv) != 4:
    print("Usage: ./image-to-ascii.py <image_file> <max_height> <character_width_to_height_ratio>")
    sys.exit()
f, h, r = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])

###############################################################

path = "./%sImages" % f

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

###############################################################

vidcap = cv2.VideoCapture(f)
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(path + "/frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  #print('Read a new frame: ', success)
  count += 1
print("Done writing images")

###############################################################

path2 = "./%sAsciiFiles" % f

if (input2 == "y"):
    try:
        os.mkdir(path2)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

###############################################################

def generateAscii(f, h, r):
    img = Image.open(path + "/" + f)
    img = img.convert("L") #convert to greyscale

    (x,y) = img.size
    newsize = (int(x/y*h*r), h) #width is r*height, image aspect-ratio is kept
    img = img.resize(newsize, Image.ANTIALIAS)

    str = ""
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            lum = 255-img.getpixel((x,y))
            str += greyscale[(lum//24)] #24 pixels per tonal range
        str += "\n"

    if (input2 == "y"):
        f = open(path2 + "/" + (f.split(".")[0] + ".txt"), "w")
        f.write(str)
        f.close()
    print(str)

while True:
    if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
        break
    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            #print(os.path.join(path, filename))
            generateAscii(filename, h, r)
        else:
            continue
    if (input1 == "n"):
        break
    else:
        continue
