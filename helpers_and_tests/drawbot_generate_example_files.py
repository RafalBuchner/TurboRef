"""
code for animation by Just Van Rossum
you can find tutorial how to make this animation here
https://vimeo.com/149247423
"""
from drawBot import *
import os,shutil, random
from yaml import load, dump
colors = [
	(0.0, 0.6970626382848859, 0.644083314259556, 1.0),
	(1.0, 0.24574654764629586, 0.07129015030136568, 1.0),
	(0.018204013122758832, 0.6800030518043794, 1.0, 1.0),
	(0.7522850385290303, 0.7797817959868772, 0.8434882124055848, 1.0),
	(0.019394216830701153, 0.012848096437018387, 0.15327687495231557, 1.0)
]

if not os.path.exists("./images"):
    os.mkdir('images')
else:
    shutil.rmtree("./images")
    os.mkdir('images')
imagePaths = []

for c in colors:
    wSize = randint(1,12)*100
    hSize = randint(1,12)*100
    newDrawing()
    size(wSize, hSize)
    fill(*c)
    rect(0,0,wSize, hSize)
    path = f"./images/{wSize}-{hSize}.png"
    imagePaths += [path]
    saveImage(path)

newDrawing()

CANVAS = 500
SQUARESIZE = 158
NSQUARES = 50
SQUAREDIST = 6

width = NSQUARES * SQUAREDIST

NFRAMES = 50
bcColor = random.choice(colors)

rectColor = bcColor
while rectColor == bcColor:
    rectColor = random.choice(colors)
strokeWidthValue = randint(1,4)
for frame in range(NFRAMES):
    newPage(CANVAS, CANVAS)
    frameDuration(1/20)
    stroke(None)
    fill(*bcColor)
    rect(0, 0, CANVAS, CANVAS)
    
    phase = 2 * pi * frame / NFRAMES  # angle in radians
    startAngle = 90 * sin(phase)
    endAngle = 90 * sin(phase + 0.5 * pi)

    translate(CANVAS/2 - width / 2, CANVAS/2)

    fill(*rectColor)
    strokeWidth(strokeWidthValue)
    stroke(*bcColor)

    for i in range(NSQUARES + 1):
        f = i / NSQUARES
        save()
        translate(i * SQUAREDIST, 0)
        scale(0.7, 1)
        rotate(startAngle + f * (endAngle - startAngle))
        rect(-SQUARESIZE/2, -SQUARESIZE/2, SQUARESIZE, SQUARESIZE)
        restore()

saveImage("./images/StackOfSquaresAnimation.gif")


### simple image objects
import os

class TurboElement(object):
	"""docstring for TurboElement"""
	def __init__(self, position, scale, rotation):
		self.position = position
		self.scale = scale
		self.rotation = rotation

class TurboTextBox(TurboElement):
	"""docstring for TurboImage
		
		fontProperties:

		fontSize = int
		fontName = str

	"""
	def __init__(self, text, fontProperties, position, scale, rotation):
		super(TurboImage, self).__init__(position, scale, rotation)
		self.text = text
		self.fontProperties = fontProperties

class TurboImage(TurboElement):
	"""docstring for TurboImage"""
	def __init__(self, path, position, scale, rotation):
		super(TurboImage, self).__init__(position, scale, rotation)
		self.pathExists = False
		self.path = path

	def validatePath(self, value):
		if if os.path.exist(value):
			self.pathExists = True
			value = os.path.abspath(value)
		else: 
			self.pathExists = False
		return value
	@path.setter
	def path(self, value):
		# assert if not a string!!!!

		self.path = path



if __name__ == "__main__":
    imageList = [for p in imagePaths]
		

