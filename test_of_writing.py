from PIL import Image, ImageDraw, ImageFont
from graphic_library import *

IMAGE_WIDTH = 2500
IMAGE_HEIGHT = 2500
FONTSIZE = int(0.04 * IMAGE_HEIGHT)


font = ImageFont.truetype("arial.ttf",FONTSIZE)
horizontal_image = Image.new("RGB",(IMAGE_WIDTH, IMAGE_HEIGHT),"blue")

draw = ImageDraw.Draw(horizontal_image)

draw.text((0,0),"Set 1,13 Rep A Colony 1 Day 1 Method brightfield Media LB Rise 32.5", font = font)
horizontal_image.show()