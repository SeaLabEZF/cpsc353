from PIL import Image
import math
import sys

######################################################
# Function: decode                                   #
# Input: img                                         #
# Output: converted_msg                              #
#                                                    #
# Description:                                       #
# Takes img and gets width and height from it.       #
# Creates col and row based on width and height      #
# respectively extracts the mesage size from the     #
# image with extractor function converts it back     #
# to a base 10 number then extracts the message      #
# based on the message size obtained in the first    #
# 11 pixels.                                         #
######################################################
def decode(img):
    width, height = img.size
    col = width-1
    row = height-1

    msg_size = extractor(width, col, row)
    msg_size = msg_size[:32]
    msg_size = int(msg_size,2)

    col = width-12
    pixel_amount = math.ceil(msg_size/3)
    msg = extractor(width, col, row, pixel_amount)
    msg = msg[:msg_size]
    converted_msg = ''.join(chr(int(msg[i:i+8],2)) for i in range(0, len(msg),8))
    return converted_msg

######################################################
# Function: extractor                                #
# Input: width, col, row, finish(default = 11)       #
# Output: information_bin                            #
#                                                    #
# Description:                                       #
# Takes width input of the image, current column,    #
# current row, how many pixels to traverse, and      #
# extracts information (in binary) by calling the    #
# getpixel function to access RGB, reads the LSB     #
# and stores it within information_bin as a string   #
######################################################
def extractor(width, col, row, finish = 11):

    information_bin = ''
    for i in range(finish):
        r, g, b = img.getpixel((col, row))
        information_bin += str(bin(r))[-1]
        information_bin += str(bin(g))[-1]
        information_bin += str(bin(b))[-1]
        if col is 0:
            col = width
            row = row - 1
        col = col - 1
    return information_bin

######################################################
# Function: encode                                   #
# Input: img, msg                                    #
# Output: N/A                                        #
#                                                    #
# Description:                                       #
# Takes img and stores width and height information, #
# col and row are derived from the width and height  #
# message length is calulated and converted to binary#
# full message is then converted to binary. These    #
# are both put into the image via the injector       #
# function.                                          #
######################################################
def encode(img, msg):
    width, height = img.size
    col = width-1
    row = height-1

    msg_len = len(msg) * 8
    msg_len_bin = str(bin(msg_len))
    msg_len_bin = msg_len_bin[2:]
    msg_len_bin = ("0" * 32) + msg_len_bin + "0"
    msg_len_bin = msg_len_bin[-33:]
    print(msg_len_bin)

    msg_bin = str(bin(int.from_bytes(msg.encode(), 'big')))
    msg_bin = msg_bin[:1] + msg_bin[2:]

    pixel_amount = int(msg_len/3)
    print(pixel_amount)
    print("injecting size")
    injector(width, col, row, 11, msg_len_bin)
    print("size injected")
    col = width-12
    print("injecting message")
    injector(width, col, row, pixel_amount, msg_bin)
    print("message injected")
    
######################################################
# Function: injector                                 #
# Input: width, col, row, finish, bin_file           #
# Output: N/A                                        #
#                                                    #
# Description:                                       #
# Takes width input of the image, current column,    #
# current row, how many pixels to traverse, and      #
# inject information (in binary) calls the           #
# getpixel function to access current RGB, modifies  #
# them with the string of bits from bin_file by      #
# by calling the newRGB function                     #
######################################################
def injector(width, col, row, finish, bin_file):
    bin_file_index = 0
    for i in range(finish):
        r, g, b = img.getpixel((col, row))
        r = newRGB(r, int(bin_file[bin_file_index]))
        bin_file_index += 1
        g = newRGB(g, int(bin_file[bin_file_index]))
        bin_file_index += 1
        b = newRGB(b, int(bin_file[bin_file_index]))
        bin_file_index += 1
        img.putpixel((col,row),(r,g,b))
        if col is 0:
            col = width
            row = row - 1
        col = col - 1

######################################################
# Function: newRGB                                   #
# Input: originalRGB, bit                            #
# Output: modified RGB value                         #
#                                                    #
# Description:                                       #
# This takes RGB values one by one with a bit to     #
# inject will see if the originalRGB is even         #
# if it is the value is subtracted by 1 and the      #
# injected bit is placed at the LSB.                 #
######################################################
def newRGB(originalRGB, bit):
    if(originalRGB % 2 is 1):
        return (originalRGB-1) + bit
    else:
        return originalRGB + bit

######################################################
# main                                               #
# Input: argv[n]                                     #
# Output: N/A                                        #
#                                                    #
# Description:                                       #
# where all the action happens.                      #
######################################################

if len(sys.argv) < 1:
    print("missing parameter (can has [-h|-H|-d|-D|-e|-E]?)")
elif sys.argv[1] is '-d' or sys.argv[1] is '-D':
    if sys.argv[2][-4:] is '.png':
        if sys.argv[3][-4:] is '.txt':
            img = Image.open(sys.argv[2])
            msg = decode(img)
            file = open(sys.argv[3], "w")
            file.write(msg)
            file.close()
            img.close()
            print(msg)
        else:
            print("arg[3] incorrect (can has *.txt?)")
    else:
        print("arg[2] incorrect (can has *.png?)")
elif sys.argv[1] is '-e' or sys.argv[1] is '-E':
    if sys.argv[2][-4:] is '.jpg':
        if sys.argv[3][-4:] is '.txt':
            if sys.argv[4] is not None:
                output = sys.argv[4]
                if output[-4:] is '.png':
                    output = output[:-4]
                output = output + ".png"
                img = Image.open(argv[2])
                file = open(argv[3], "r")
                msg = file.read()
                encode(img, msg)
                file.close()
                img.save(output, "PNG")
                img.close()
            else:
                print("arg[4] incorrect (can has output name?)")
        else:
            print("arg[3] incorrect (can has *.txt?)")
    else:
        print("arg[2] incorrect (can has *.jpg")
elif sys.argv[1] is '-h' or sys.argv[1] is '-H':
    print("\t\tproject.py\n")
    print("SYNOPSIS\n")
    print("\tpython3 project.py [-h|-H]\n")
    print("\tpython3 project.py [-d|-D] [image] [output-file]\n")
    print("\tpython3 project.py [-e|-E] [image] [input-file] [output-image]\n")
    print("\nDESCRIPTION\n")
    print("\tproject.py is used to ether encode or decode messages that have been stored\n")
    print("\twithin an image. The message, if decoded, will be displayed in the terminal\n")
    print("\tand outputed to a file. If encode is used the message must be placed in a text\n")
    print("\tfile and fed as an argument.")
    print("\nCOMMAND\n")
    print("\t[-h|-H] --help\t\tdisplays a short description of what the program does and how to run it.\n")
    print("\t[-d|-D] --decode\ttakes <*.png> image and a name for your output message.\n")
    print("\t[-e|-E] --encode\ttakes <*.jpg> image and a <*.txt> file as input and takes a name for your output image.\n")
else:
    print("unrecognized parameter (can has [-h|-H|-d|-D|-e|-E]?)")