# This script takes an input file listing image filenames and metadata and creates composite pictures of them
# The script expects tab-delimited files
# The first column must always be the filename, but columns after that can be varied as needed
# Captions will be created in the left->right order they appear in
# Headings you don't want included should have a & character at the start of the field
# Make sure the first character is # so it knows to skip that line when drawing images
# Separate sets of images are noted by a line break between the sets.
# THERE NEED TO BE TWO SPACES AT THE END OF THE FILE, or it won't graph the last set.

# expected command line usage is "python colony_poster.py spreadsheet.txt"


# BUGS:
# the resize checks are weird

# TODO:
# finish up making this more flexible w/r/t metadata input files

import sys
from PIL import Image, ImageDraw, ImageFont
import linecache
import re

IMAGE_WIDTH = 2500
IMAGE_HEIGHT = 2500
FONTSIZE = 50
CAPTION_VERTICAL_SPACING = 10

# this is the key for which number codes go with which species
# eventually I'd like this to be dynamic and read a reference sheet but for now it's hardcoded
SPECIES_KEY = {1:'B. subtilis 3610', 2:'B. subtilis PtapA-YFP',4:'B. atrophaeus', 5:'B. vallismortis', 7:'B. licheniformis', 9:'B. megaterium', 12:'B. lentus', 13:'B. cereus WT', 14:'B. cereus delta(tclE-H)', 15:'B. clausii', 3:'B. mojavensis', 3:'B. mojavensis', 387:'RO-NN-1', 389:'DV1-B-1' }

# start up the font object for PIL so we can draw text
font =  ImageFont.truetype("fonts/arial.ttf", FONTSIZE)

# read in spreadsheet filename
colony_sheet = open(sys.argv[1])

# let's get the column headings from the first line of the file
heading_line = linecache.getline(sys.argv[1], 1)[1:].rstrip()
COLUMN_HEADINGS = heading_line.split("\t")

def find_species_name(species_number):
	# takes a species number, returns a string with the name and genotype
	# NOT FINISHED YET OR EVEN WRITTEN
	print("it's not done yet dummy")
	try:
		output = SPECIES_KEY[species_number]
	except:
		output = False
	return output

# so we don't have to reference the input sheet constantly, let's make a class to hold metadata
class TestImage:
	def __init__(self, headings, contents):
		# Headings is a list of strings that it will use for attribute names
		# The global COLUMN_HEADINGS variable should be used here
		
		# First, make sure the table makes sense
		if len(contents) > len(headings):
			sys.exit("SOMETHING IS VERY WRONG WITH YOUR TABLE")
		
		# now make sure we're not trying to erase an important attribute
		for each_heading in headings:
			if hasattr(self, each_heading):
				sys.exit("CHANGE YOUR COLUMN NAMES, YOU'RE TRYING TO OVERWRITE SOMETHING IMPORTANT")
				
		# ok, now that's out of the way, and we can actually assign attributes
		# but let's just make sure to strip out the "don't put this in the caption" mark
		# also we'll check to see if there's actually something in that cell, and if not give it a default value
		for pos in range(len(headings)):
			temporary_heading = ""
			if headings[pos][0] == "&":
				temporary_heading = headings[pos][1:]
			else:
				temporary_heading = headings[pos]
			if contents[pos] == "":
				setattr(self, temporary_heading, "N/A")
			else:
				setattr(self, temporary_heading, contents[pos])
		
		# we'll set these later
		self.caption = "N/A"
		self.output_filename = "N/A"
		
		# see http://stackoverflow.com/questions/6735583/treat-value-of-string-as-an-attribute-name
		
	def generate_filename(self):
		# this method takes the column headings and constructs a caption for the images
		# it uses all of the metadata in the appropriate order, unless indicated otherwise
		# since we can't know ahead of time what the column identities will be, it will use the column names directly
		
		# pick out just the columns we want to talk about in the filename and caption
		columns_to_describe = []
		for each in COLUMN_HEADINGS:
			if each[0] is "&":
				continue
			else:
				columns_to_describe.append(each)
		
		# first, check if it's string or number
		# if it's a string, split on comma

		# make a filename, and try to use the expanded names of things
		# if you can't, use the abbreviated coded version
		
		# also let's build a regex search pattern ahead of time
		keyword = re.compile("colony", flags=re.IGNORECASE)
		try:
			# set output filename with species names
		except:			
			# set output filename with species numbers
			
		# make a caption, try to use expanded names, if can't, use codes
		try:
			# set caption, replacing numbers with species names
			# FUTURE EFFORTS : make it so this checks a run flag instead
			for each_heading in columns_to_describe:
				if keyword.search(each_heading) is not None:
					name = find_species_name(getattr(self,each_heading))
					setattr(self, each_heading, name)
			
			self.output_filename = " ".join([" ".join([each, getattr(self, each)]) for each in columns_to_describe])
		except:
			# set caption exactly as it's given in the input file
			self.output_filename = " ".join([" ".join([each, getattr(self, each)]) for each in columns_to_describe])
			# " ".join([" ".join([each,getattr(test,each)]) for each in types])

# the following class is kept around for reference and will be removed later
class ColonyImage:
	def __init__(self, image_name = "N/A", area = "N/A", replicate = "N/A", colony = "N/A", day = "N/A", media = "N/A", rise = "N/A", colony_set = "N/A", filename = "N/A", method = "N/A", caption = "N/A"):
		# species_name and mix_name and set_real_name are left as none because they'll be generated by referencing the key and not by input from the data sheet
		self.image_name	= image_name
		self.area = area
		self.replicate = replicate
		self.colony = colony
		self.day = day
		self.media = media
		self.rise = rise
		self.colony_set = colony_set
		self.filename = filename
		self.method = method
		self.species_name = None
		self.mix_name = None
		self.set_real_name = None
		self.caption = caption
		
		# I intend to make it so that the functions for this class are agnostic of the input formatting
		# see http://stackoverflow.com/questions/6735583/treat-value-of-string-as-an-attribute-name
		# for an example of what I need to implement
		# I need to use setattr to set the class variables
		# also i need to create a global variable describing the column names
		
	def generate_filename(self):
		# look at colony value, reference species key
		# use species name instead of number
		# for now, the key is hardcoded in the script, but make it parse a record later
		
		#first, check if it's string or number
		#if it's a string, split on comma
		#use form "mix_[species a]:[species b]"
		
		#if it's not a string, just use the colony name straight
		if self.colony[-1].isalpha() is True:
			self.colony = self.colony[:-1]
		if self.colony.isdigit() is False:
			# I think I might need to manage the input so it doesn't have flanking quote markes
			members = [int(each) for each in self.colony.split(",",1)]
			member_names = [SPECIES_KEY[each] for each in members]
			self.mix_name = " ".join(["Mix of",member_names[0],member_names[1]])
		else:
			self.mix_name = SPECIES_KEY[int(self.colony)]
		
		# I think I might need to manage the input so it doesn't have flanking quote marks
		if self.colony_set.isdigit() is False:
			set_members = [int(each) for each in self.colony_set.split(",",1)]
			set_member_names = [SPECIES_KEY[each] for each in set_members]
			self.set_real_name = ",".join(["Mix of",set_member_names[0],set_member_names[1]])
		else:
			self.set_real_name = SPECIES_KEY[int(self.colony_set)]
		
		#make a filename, and try to use the expanded names of things
		#if you can't, use the abbreviated coded version
		try:
			self.filename = ' '.join(["Set -",self.set_real_name,"; Rep -",self.replicate,"; Colony -",self.mix_name,"; Day -",self.day,"; Method -",self.method,"; Media -",self.media,"; Rise -",self.rise,"; composite"]) +".jpg"
		except:			
			self.filename = ' '.join(["Set - ",self.colony_set,"; Rep -",self.replicate,"; Colony -",self.colony,"; Day -",self.day,"; Method -",self.method,"; Media -",self.media,"; Rise -",self.rise,"; composite"]) +".jpg"
		
		# make a caption, try to use expanded names, if can't, use codes
		try:
			self.caption = ' '.join(["Day -",self.day, "; Colony -",self.mix_name])
		except:
			self.caption = ' '.join(["Set -",self.colony_set,"; Rep -",self.replicate,"; Colony -",self.colony,"; Day -",self.day,"; Method -",self.method,"; Media -",self.media])

def check_length(text, image_width):
	# YOU NEED TO PASS AN IMAGE WIDTH TO THE CHECKER FUNCTION SO IT KNOWS WHAT LENGTH TO CHECK TO
	# EXPECTED USAGE:
		# called by wrap_text()
		# give it a string to length-check and a width to check it against
	text_details = font.getsize(text)
	text_width = text_details[0]
	text_height = text_details[1]
	if text_width > image_width:
		return False # text width greater than image width
	else:
		return True # text width less than image width

def wrap_text(text, image_width):
	print("wrap text called")
	# I DON'T KNOW WHY BUT IT'S NOT WRAPPING CORRECTLY

	# YOU NEED TO PASS AN IMAGE WIDTH TO THE WRAPPING FUNCTION SO IT KNOWS WHAT TO WRAP TO
	# EXPECTED USAGE:
		# expects a string
		# returns a list where each entry is whole-word sets of wrapped text
	string = ""
	scratch = text
	output = []
	if check_length(scratch, image_width) is True:
		output.append(scratch)
	while check_length(scratch, image_width) is False:
		# move to the start of the next previous word
		string = scratch[-1] + string # STRING IS THE BACK HALF
		scratch = scratch[0:-1] # SCRATCH IS THE FRONT HALF
		test = 0
		# test to make sure there's at least one space and the last isn't a hyphen or dash
		# if scratch[-1] in ("-", "—", "–" ,"-"):
		#	endhyphen += 1
		for letter in scratch:
			if letter == " ":
				test += 1
		# if there's not at least one space, split the word and add hyphens
		if test == 0 :
			string = "-" + scratch[-1] + string
			scratch = scratch[0:-1] + "-"
		# now, backtrack until you hit the first space or hyphen
		if test == 0:
			if scratch[-1] is "-":
				string = string
			elif scratch[-1] is not "-":
				while scratch[-1] is not "-":
					string = scratch[-1] + string
					scratch = scratch[0:-1]
		else:
			while scratch[-1] is not " ":
				string = scratch[-1] + string
				scratch = scratch[0:-1]
		if check_length(scratch, image_width) is True:
			output.append(scratch) # STICK THE FRONT HALF ON THE OUTPUT
			scratch = string
			if check_length(string, image_width) is True:
				output.append(string)
			else:
				string = ""
		# print(check_length(scratch, image_width))

	# output.append(string) # STICK THE BACK HALF ON THE OUTPUT
	print("output is ")
	print(output)
	return output

# let's make a function that will do all the image processing for us
def draw_images(colony_list, direction):
	# takes a list of colony objects, then graphs them side by side
	image_list = []
	for each in colony_list:
		# open up the image file noted by the item in the list
		new_picture = Image.open(each.image_name)
		width_height = new_picture.size
		width = width_height[0]
		height = width_height[1]
		
		# WARNING: THIS IS A TROUBLE SPOT, IT REFERENCES A PRESUPPOSED ATTRIBUTE
		if each.method == "fluor":
			new_picture = new_picture.transpose(Image.ROTATE_180) # because the digital camera is upside down to the fluoresence camera, so we need the same orientation for all pictures
		
		# these 2500 and 1000 values are hardcoded for now but might be made dynamic later
		# 2500x2500 is a good size that retains the central colony features of our digicam image at full size taken with the camera stage at 32.5 cm above the table
		if width > 2500 and height > 2500:
			#crop it
			top = int((height - IMAGE_HEIGHT)/2)
			bottom = int(top + IMAGE_HEIGHT)
			left = int((width - IMAGE_WIDTH)/2)
			right = int(left + IMAGE_WIDTH)
			new_picture = new_picture.crop((left,top,right,bottom))
		elif width > 2500 and height < 2500:
			# crop to height
			left = int((width - height)/2)
			right = int(left + height)
			new_picture = new_picture.crop((left,0,right,0))
		elif width < 2500 and height > 2500:
			# crop to width
			top = int((height - width)/2)
			bottom = int(top + width)
			new_picture = new_picture.crop(0,top,0,bottom)

		# resize the pictures so our composites aren't mega huge
		# I think I fucked up here, I think it should be >=, not <, but I get weird results when I change it
		# bugfix later
		if width < 2500 and height == width:
			new_width = int(float(1000))
			new_height = int(float(1000))
			new_picture = new_picture.resize((new_width,new_height),Image.ANTIALIAS)
		elif width < 2500 and height != width:
			ratio = height / width
			new_width = int(float(1000))
			new_height = int(ratio * new_width)
			new_picture = new_picture.resize((new_width,new_height),Image.ANTIALIAS)
		image_list.append(new_picture)
	
	total_width = 0
	total_height = 0
	max_width = 0
	max_height = 0
	
	captioned_image_list = []
	# ok, now let's add captions
	count = 0
	for each_img in image_list:
		# add the title below it
		# get size of filename as an image
		# draw appropriate height box
		# put box below image, add filename text
		
		# later, abstract this out and put it in graphic_library
		# WARNING, THIS IS A TROUBLE SPOT, IT REFERENCES PRESUPPOSED ATTRIBUTES
		try:
			wrapped_caption = wrap_text(colony_list[count].caption, each_img.size[0])
			# IT'S A PIL OBJECT NOT MY IMAGE CLASS OBJECT
		except:
			wrapped_caption = wrap_text(colony_list[count].filename, each_img.size[0])
			# IT'S A PIL OBJECT NOT MY IMAGE CLASS OBJECT
		
		total_caption_height = 0
		
		for each_stub in wrapped_caption:
			#print(each_stub)
			stub_dimensions = font.getsize(each_stub)
			total_caption_height += stub_dimensions[1]
		total_caption_height += CAPTION_VERTICAL_SPACING * (len(wrapped_caption) - 1)
		# create the mini canvas for the caption
		caption_canvas = Image.new("RGB", (each_img.size[0], total_caption_height), "black")
		height_pos = 0
		draw = ImageDraw.Draw(caption_canvas)
		for each_stub in wrapped_caption:
			draw.text((0,height_pos), each_stub, font = font)
			stub_dimension = font.getsize(each_stub)
			#print(stub_dimension)
			#print(each_stub)
			height_pos += stub_dimension[1] + CAPTION_VERTICAL_SPACING
			
		#caption_canvas.show()
		print(caption_canvas.size)
		
		# create a composite canvas for the image and the caption
		composite_canvas = Image.new("RGB", (each_img.size[0], each_img.size[1] + total_caption_height), "black")
		
		# add the image and the caption to the canvas
		composite_canvas.paste(each_img, (0, 0))
		composite_canvas.paste(caption_canvas, (0, each_img.size[1]))
		captioned_image_list.append(composite_canvas)
		#composite_canvas.show()
		
		count += 1

	image_list = []
	# now, start stacking the images
	print("Printing image, please wait...")
	# start with a horizontal arrangement
	if direction == "horizontal":
		for each_img in captioned_image_list:
			if each_img.size[0] > max_width:
				max_width = each_img.size[0]
			if each_img.size[1] > max_height:
				max_height = each_img.size[1]
		total_width = len(captioned_image_list) * max_width
		total_height = len(captioned_image_list) * max_height
		#print(total_width)
		horizontal_image = Image.new("RGB",(total_width, max_height),"black")
		number_of_images = len(captioned_image_list)
		count = 0
		for each_image in captioned_image_list:
			horizontal_image.paste(each_image,(0+count*max_width,0))
			count += 1
		horizontal_image.save(colony_list[0].filename)
	# now the case of the vertical arrangement
	elif direction == "vertical":
		for each_img in captioned_image_list:
			if each_img.size[0] > max_width:
				max_width = each_img.size[0]
			if each_img.size[1] > max_height:
				max_height = each_img.size[1]
		total_width = len(image_list) * max_width
		total_height = len(image_list) * max_height
		horizontal_image = Image.new("RGB",(total_height, max_width),"black")
		number_of_images = len(captioned_image_list)
		count = 0
		for each_image in captioned_image_list:
			vertical_image.paste(each_image,(0,0+count*max_height))
			count += 1
		vertical_image.save(colony_list[0].filename)
		

# phew, that's out of the way. now we can actually do stuff with that stuff we defined

# now we're going to start paging through the input document to find the images we need to tile
colony_list = []

for line in colony_sheet:
	if line.rstrip() is "":
		try:
			draw_images(colony_list,"horizontal")
		except:
			print("couldn't print the image, sorry")
		# clear the colony list
		colony_list = []
		continue

	if line[0] is "#":
		continue

	# manage the line, split it up into proper variables
	# WARNING, THIS IS A TROUBLE SPOT, IT PRESUPPOSES ATTRIBUTES
	line = line.rstrip()
	temporary_list = line.split("\t")
	image_name = temporary_list[0]
	replicate = temporary_list[1]
	colony = temporary_list[2]
	colony_no_quotes = [each for each in colony if each not in '"']
	colony = ''.join(colony_no_quotes)
	colony_set = temporary_list[3]
	colony_set_no_quotes = [each for each in colony_set if each not in '"']
	colony_set = ''.join(colony_set_no_quotes)
	day = temporary_list[4]
	media = temporary_list[5]
	rise = temporary_list[6]
	method = temporary_list[7]
	
	# construct the new filename from all those variables you just split up
	new_image = ColonyImage(image_name = image_name, replicate = replicate, colony = colony, day = day, media = media, rise = rise, colony_set = colony_set, method = method)
	new_image.generate_filename()
	colony_list.append(new_image)
