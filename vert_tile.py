# take output from colony_poster_implicit.py
# get the list of filenames
# this will tile them vertically and make sure they have their filenames above them.

import sys
from PIL import Image, ImageDraw

timecourse_names = open(sys.argv[1])

RESIZED_WIDTH = 700

def draw_images(colony_list, direction):
	# takes a list of colony objects, then graphs them side by side
	filename = "composite" + colony_list[0].rstrip()
	image_list = []
	#print(colony_list)
	for each in colony_list:
		# open up the image file noted by the item in the list
		new_picture = Image.open(each)
		if new_picture.size[0] > 2500:
			ratio = new_picture.size[1] / new_picture.size[0]
			new_width = int(float(RESIZED_WIDTH))
			new_height = int(ratio * new_width)
			new_picture = new_picture.resize((new_width,new_height),Image.ANTIALIAS)
		image_list.append(new_picture)
	
	total_width = 0
	total_height = 0
	max_width = 0
	max_height = 0
	
	#now, start stacking the images
	print("Printing image, please wait...")
	#start with a horizontal arrangement
	if direction == "horizontal":
		for each_img in image_list:
			if each_img.size[0] > max_width:
				max_width = each_img.size[0]
			if each_img.size[1] > max_height:
				max_height = each_img.size[1]
		total_width = len(image_list) * max_width
		total_height = len(image_list) * max_height
		horizontal_image = Image.new("RGB",(total_width, max_height),"black")
		number_of_images = len(image_list)
		count = 0
		for each_image in image_list:
			horizontal_image.paste(each_image,(0+count*max_width,0))
			count += 1
		horizontal_image.save(filename)
	#now the case of the vertical arrangement
	elif direction == "vertical":
		for each_img in image_list:
			if each_img.size[0] > max_width:
				max_width = each_img.size[0]
			if each_img.size[1] > max_height:
				max_height = each_img.size[1]
		total_width = len(image_list) * max_width
		total_height = len(image_list) * max_height
		vertical_image = Image.new("RGB",(max_width, total_height),"black")
		number_of_images = len(image_list)
		count = 0
		for each_image in image_list:
			vertical_image.paste(each_image,(0,0+count*max_height))
			count += 1
		vertical_image.save(filename)

images_to_tile = []

for line in timecourse_names:
	if line.rstrip() is "":
		print(images_to_tile)
		draw_images(images_to_tile,"vertical")
		images_to_tile = []
		continue

	if line[0] is "#":
		continue

	line = line.rstrip()
	images_to_tile.append(line)