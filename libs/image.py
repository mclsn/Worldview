class image:

	def CropProfile(self, path, size):
		from PIL import Image

		im = Image.open(path)
		size = (size, size)
		im.thumbnail(size, Image.ANTIALIAS)
		width, height = im.size[0], im.size[1]
		sizeB = (0,0)

		if(width >= height):
			sizeB = (height,height)
		else:
			sizeB = (width,width)

		background = Image.new('RGBA', sizeB, (255, 255, 255, 0))
		background.paste(im)
		background.save(path, "JPEG")
		return True
