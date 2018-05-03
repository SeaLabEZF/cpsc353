from PIL import Image
import math
import sys

######################################################
# Function: Main                                     #
######################################################
def main():
    if len(sys.argv) == 1:
        print("missing parameter (can has [-h|-H|-d|-D|-e|-E]?)")
    elif len(sys.argv) == 2 and (sys.argv[1] == '-h' or sys.argv[1] == '-H'):
        help_menu()
    elif len(sys.argv) == 4 and (sys.argv[1] == '-d' or sys.argv[1] == '-D'):
        inImage = sys.argv[2]
        infile = sys.argv[3]
        if inImage[-4:] == ".png" and infile[-4:] == ".txt":
            img = Image.open(inImage)
            msg = decode(img)
            file = open(infile, "w")
            file.write(msg)
            file.close()
            img.close()
            print("Encoded message stored in", infile)
        else:
            print("issue with last two arguments, check file extension (*.png , *.txt)")
    elif len(sys.argv) == 5 and (sys.argv[1] == '-e' or sys.argv[1] == '-E'):
        inImage = sys.argv[2]
        infile = sys.argv[3]
        outImage = sys.argv[4]
        if inImage[-4:] == ".jpg" and infile[-4:] == ".txt":
            if outImage[-4:] == ".png":
                outImage = outImage[:-4]
            outImage = outImage + ".png"
            file = open(infile)
            msg = file.read()
            file.close()
            img = Image.open(inImage)
            encode(img, msg)
            img.save(outImage, "PNG")
        else:
            print("issue with last three arguments, check file extensions (*.jpg , *.txt , *)")
    elif len(sys.argv) > 5:
        print("Too many arguments, what are you doing?! STAHP!!!!")
    else:
        print("Check parameters (python3 project.py -h)")

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

    msg_size = extractor(img, width, col, row)
    msg_size = msg_size[:32]
    msg_size = int(msg_size,2)

    col = width-12
    pixel_amount = math.ceil(msg_size/3)
    msg = extractor(img, width, col, row, pixel_amount)
    msg = msg[:msg_size]
    converted_msg = ''.join(chr(int(msg[i:i+8],2)) for i in range(0, len(msg),8))
    return converted_msg

######################################################
# Function: extractor                                #
# Input: img, width, col, row, finish(default = 11)  #
# Output: information_bin                            #
#                                                    #
# Description:                                       #
# Takes width input of the image, current column,    #
# current row, how many pixels to traverse, and      #
# extracts information (in binary) by calling the    #
# getpixel function to access RGB, reads the LSB     #
# and stores it within information_bin as a string   #
######################################################
def extractor(img, width, col, row, finish = 11):

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

    msg_bin = str(bin(int.from_bytes(msg.encode(), 'big')))
    msg_bin = msg_bin[:1] + msg_bin[2:]

    pixel_amount = int(msg_len/3)
    print("injecting size")
    injector(img, width, col, row, 11, msg_len_bin)
    print("size injected")
    col = width-12
    print("injecting message")
    injector(img, width, col, row, pixel_amount, msg_bin)
    print("message injected")
    
######################################################
# Function: injector                                 #
# Input: img, width, col, row, finish, bin_file      #
# Output: N/A                                        #
#                                                    #
# Description:                                       #
# Takes width input of the image, current column,    #
# current row, how many pixels to traverse, and      #
# inject information (in binary) calls the           #
# getpixel function to access current RGB, modifies  #
# them with the string of bits from bin_file by      #
# by calling the new_RGB function                     #
######################################################
def injector(img, width, col, row, finish, bin_file):
    bin_file_index = 0
    for i in range(finish):
        r, g, b = img.getpixel((col, row))
        r = new_RGB(r, int(bin_file[bin_file_index]))
        bin_file_index += 1
        g = new_RGB(g, int(bin_file[bin_file_index]))
        bin_file_index += 1
        b = new_RGB(b, int(bin_file[bin_file_index]))
        bin_file_index += 1
        img.putpixel((col,row),(r,g,b))
        if col is 0:
            col = width
            if row is 0:
                print("Text too large, partial encode.")
                break
            row = row - 1
        col = col - 1

######################################################
# Function: new_RGB                                  #
# Input: original_RGB, bit                           #
# Output: modified RGB value                         #
#                                                    #
# Description:                                       #
# This takes RGB values one by one with a bit to     #
# inject will see if the original_RGB is odd         #
# if it is the value is subtracted by 1 and the      #
# injected bit is placed at the LSB.                 #
######################################################
def new_RGB(original_RGB, bit):
    if original_RGB % 2 is 1:
        return original_RGB - 1 + bit
    return original_RGB + bit

######################################################
# Function: help_menu                                #
# Input: N/A                                         #
# Output: N/A                                        #
#                                                    #
# Description:                                       #
# Outputs a help menu for the program.               #
######################################################

def help_menu():
    print("\t\tproject.py\n")
    print("SYNOPSIS\n")
    print("\tpython3 project.py [-h|-H]\n")
    print("\tpython3 project.py [-d|-D] [image] [output-file]\n")
    print("\tpython3 project.py [-e|-E] [image] [input-file] [output-image]\n")
    print("\nDESCRIPTION\n")
    print("\tproject.py is used to ether encode or decode messages that have been stored\n")
    print("\twithin an image. The message, if decoded, message will be placed in your output\n")
    print("\tfile. If encode is used the message must be placed in a text file and fed as an argument.\n")
    print("\tThis program does not support multi-image injection.\n")
    print("\nCOMMAND\n")
    print("\t[-h|-H] --help\t\tdisplays a short description of what the program does and how to run it.\n")
    print("\t[-d|-D] --decode\ttakes <*.png> image and a name for your output message.\n")
    print("\t[-e|-E] --encode\ttakes <*.jpg> image and a <*.txt> file as input and takes a name for your output image.\n")

if __name__ == '__main__':
    main()
