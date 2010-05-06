##
## This layer is for a collection of 2D objects
##

class ObjectLayer():
	def __init__(self):
		self._objects = []
		
	def Add(self, *objects):
		self._objects.extend(objects)
		if len(objects)==1:
			return objects[0]
		return objects
		
	def Remove(self, *objects):
		for obj in objects:
			self._objects.remove(obj):
		if len(objects)==1:
			return objects[0]
		return objects
		
	def Draw(self):
		"""Draw all the objects"""
		for obj in self._objects:
			obj.Draw()
			
	