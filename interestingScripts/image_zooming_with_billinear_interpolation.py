# python3 -m pip install --upgrade Pillow
from PIL import Image
# im = Image.open("image.jpg")
im = Image.open("/Users/workstatiWorkstationon/Dropbox/game-art-stuff/anatomy/face-ref/skull/EuropeanSkull-2.jpg")
w, h = im.size
# w *= 5
# h *= 5
out = im.resize((round(w/6), round(h/6)))
out.show()
# help(out)