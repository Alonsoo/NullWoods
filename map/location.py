import math
from panda3d.core import NodePath

from trees.tree import Tree
from trees.noiseTree import NoiseTree
from map.clearing import ClearingCircle


class Location:

	def __init__(self):
		self.visited = False
		self.spawnDistance = 3200
		self.nodePath = NodePath('LocationNode')
		self.clearing = None


	def build(self):
		pass

	def update(self, info):
		pass


	def load(self):
		self.nodePath.reparentTo(render)

	def unload(self):
		self.nodePath.detachNode()


	def setPos(self, x, y, z, node = None):
		if node == None:
			self.nodePath.setPos(x, y, z)
		else:
			p = node.getP()
			node.setP(0) # kind of ugly fix, should revisit
			self.nodePath.setPos(node, x, y, 0)
			self.nodePath.setZ(z) # make sure z positioning is not camera heading dependent
			node.setP(p)

		if self.clearing != None:
			self.clearing.setPos(self.getX(), self.getY())


	def getX(self):
		return self.nodePath.getX()

	def getY(self):
		return self.nodePath.getY()



class NoiseTreeSpot(Location):

	def __init__(self):
		self.trees = []
		self.noiseTree = None
		Location.__init__(self)


	def build(self):
		n = 12
		for i in range(n):
			angle = (math.pi * 2) * i / n  +  (math.pi/n)
			r = 700	

			x = r * math.cos(angle)
			y = r * math.sin(angle)

			tree = Tree((x, y, 20))
			tree.loadInto(self.nodePath)
			self.trees.append(tree)

		self.noiseTree = NoiseTree((0,0,0), 130)
		self.noiseTree.loadInto(self.nodePath)

		self.clearing = ClearingCircle(self.nodePath.getX(), self.nodePath.getY(), 800)


	def update(self, info):
		self.noiseTree.update(info)





