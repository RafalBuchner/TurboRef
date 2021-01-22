### simple image objects
import os
import ruamel.yaml
import sys, pprint

TURBOVERSION = "0.0.0.1" # figure out how to import this
FILEEXT = ".turboref"

__DEF_FONTPROPERTIES__ = dict(size=14, font="Georgia", color=(1, 1, 1, 1))
__DEF_CANVASSIZE__ = (500, 500)
__DEF_ELEMENT_VALUES__ = dict(
			canvasSize={"width":__DEF_CANVASSIZE__[0],"height":__DEF_CANVASSIZE__[1]},
			path=None,
			text="",
			fontProperties=__DEF_FONTPROPERTIES__,
			position=dict(x=0,y=0),
			scale=1,
			rotation=0,
			groupnames=[]
		)

class TurboReferenceElement:
	
	def __init__(self):
		self.canvas = TurboCanvasElement(__DEF_CANVASSIZE__)
		self.path = None
	
	def load(self, path):
		self.path = path
		file_obj = open(path, "r")
		yaml = ruamel.yaml.YAML()
		yaml.indent(mapping=4, sequence=8, offset=4)
		yaml.explicit_start = True
		yaml.preserve_quotes = True
		data = yaml.load(file_obj.read())
		
		canvasSize = data.get("canvasSize", __DEF_ELEMENT_VALUES__['canvasSize'])

		self.canvas = TurboCanvasElement((canvasSize['width'], canvasSize['height']))
		for elementData in data.get('elements', []):
			element = self.__loadElementFromDict(elementData)
			self.canvas._addElement(element)



	def __loadElementFromDict(self, data):
		assert data.get("type") is not None, f"ERROR, unknown type of data:\n\n{data}"
		position = data.get("position",__DEF_ELEMENT_VALUES__['position'])
		scale = data.get("scale",__DEF_ELEMENT_VALUES__['scale'])
		rotation = data.get("rotation",__DEF_ELEMENT_VALUES__['rotation'])
		groupnames = data.get("groupnames",__DEF_ELEMENT_VALUES__['groupnames'])
		position = [position['x'],position['y']]
		if data.get("type") == "image":
			path = data.get("path",__DEF_ELEMENT_VALUES__['path'])
			return TurboImageElement(path, position, scale, rotation, groupnames)
		if data.get("type") == "textbox":
			text = data.get("text",__DEF_ELEMENT_VALUES__['text'])
			fontProperties = data.get("fontProperties",__DEF_ELEMENT_VALUES__['fontProperties'])
			return TurboTextBoxElement(text, position, fontProperties, scale, rotation, groupnames)

	def save(self, savepath=None):
		if savepath is None:
			assert self.path is not None, "Error, reference file path is not set."
			self.__dump(self.path)
		else:
			self.__dump(savepath)

	def __dump(self, path):
		file_obj = open(path, "w")
		if os.path.splitext(path)[-1] != FILEEXT:
			path = os.path.splitext(path)[0]+FILEEXT

		yaml = ruamel.yaml.YAML()
		yaml.indent(mapping=4, sequence=8, offset=4)
		yaml.explicit_start = True
		yaml.preserve_quotes = True
		yaml.dump(canvas.getDict(), file_obj)



class TurboCanvasElement:
	
	def __init__(self, canvasSize, elements=[]):
		assert isinstance(elements, list), "elements parameter has to be list type"
		self.elements = elements
		self.canvasSize = canvasSize
		self.type = 'canvas'
	
	def _addElement(self, element):
		self.updateCanvas()
		self.elements.append(element)

	def addImage(self, path, position, scale=1, rotation=0):
		self._addElement( 
				TurboImageElement(path, position, scale, rotation)
			)

	def addTextBox(self, text, position, fontProperties=None, scale=1, rotation=0):
		if fontProperties is None:
			fontProperties = __DEF_FONTPROPERTIES__

		self._addElement( 
				TurboTextBoxElement(text, position, fontProperties, scale, rotation)
			)

	def deleteElementByIndex(self, index):
		self.updateCanvas()
		del self.elements[index]

	def updateCanvas(self):
		pass

	def getDict(self):
		return dict(
			INFO=dict(appVersion=TURBOVERSION),
			canvasSize=dict(width=self.width, height=self.height),
			elements=[e.getDict() for e in self.elements]
			)

	@property
	def canvasSize(self):
		return self._canvasSize

	@property
	def width(self):
		return self.canvasSize[0]

	@property
	def height(self):
		return self.canvasSize[1]

	@canvasSize.setter
	def canvasSize(self, value):
		self._canvasSize = value


class TurboBaseElement:
	"""docstring for TurboBaseElement"""
	def __init__(self, position, scale, rotation, groupnames):
		self.position = position
		self.scale = scale
		self.rotation = rotation
		self.groupnames = groupnames
		self.type = None

	def getDict(self):
		NotImplemented

	@property
	def position(self):
		return self._position

	@property
	def x(self):
		return self.position[0]

	@property
	def y(self):
		return self.position[1]

	@position.setter
	def position(self, value):
		self.x, self.y = value
		self._position = value

	@x.setter
	def x(self, value):
		if hasattr(self, "position"):
			self.position[0] = value
		self._x = value
	
	@y.setter
	def y(self, value):
		if hasattr(self, "position"):
			self.position[1] = value
		self._y = value



class TurboTextBoxElement(TurboBaseElement):
	"""docstring for TurboImageElement
		
		fontProperties:

		fontSize = int
		fontName = str

	"""
	def __init__(self, text, position, fontProperties, scale, rotation, groupnames=[]):
		super().__init__(position, scale, rotation, groupnames)
		self.text = text
		self.fontProperties = fontProperties
		self.type = 'textbox'

	def getDict(self):
		asDict = dict(
				text=self.text,
				fontProperties=self.fontProperties,
				position=dict(x=self.x,y=self.y), 
				scale=self.scale, 
				rotation=self.rotation, 
				type=self.type
			)
		if self.groupnames != []:
			asDict['groupnames'] = self.groupnames
		return asDict

class TurboImageElement(TurboBaseElement):
	"""docstring for TurboImageElement"""
	def __init__(self, path, position, scale, rotation, groupnames=[]):
		super().__init__(position, scale, rotation, groupnames)
		self.pathExists = False
		self.path = path
		self.type = 'image'

	def validatePath(self, value):
		if os.path.exist(value):
			self.pathExists = True
			value = os.path.abspath(value)
		else: 
			self.pathExists = False
		return value
	
	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, value):
		self._path = value

	def getDict(self):
		asDict = dict(
				path=self.path,
				position=dict(x=self.x,y=self.y),  
				scale=self.scale, 
				rotation=self.rotation, 
				type=self.type
			)
		if self.groupnames != []:
			asDict['groupnames'] = self.groupnames
		return asDict


if __name__ == '__main__':
	print(TURBOVERSION)

