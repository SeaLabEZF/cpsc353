Name: Sean Wulwick

		project.py

SYNOPSIS

	python3 project.py [-h|-H]

	python3 project.py [-d|-D] [image] [output-file]

	python3 project.py [-e|-E] [image] [input-file] [output-image]


DESCRIPTION

	project.py is used to ether encode or decode messages that have been stored

	within an image. The message, if decoded, message will be placed in your output

	file. If encode is used the message must be placed in a text file and fed as an argument.


COMMAND

	[-h|-H] --help		displays a short description of what the program does and how to run it.

	[-d|-D] --decode	takes <*.png> image and a name for your output message.

	[-e|-E] --encode	takes <*.jpg> image and a <*.txt> file as input and takes a name for your output image.

Sample input:

python3 project.py -e @w3$0m31m@g3.jpg hackingscript.txt sUpperSeecreet.png

python3 project.py -d sUpperSeecreet.png seecreeet.txt

python3 project.py -h
