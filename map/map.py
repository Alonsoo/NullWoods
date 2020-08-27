import math
from random import uniform, gauss
from direct.task import Task

from trees.tree import Tree

class Map:

	clearings = []

	def registerClearing(clearing):
		Map.clearings.append(clearing)

	def unregisterClearing(clearing):
		Map.clearings.remove(clearing)





class MapTreeGen:

	def __init__(self, minRadius, maxRadius, visionRadius, laodingRadus, anchor):
		self.minRadius = minRadius
		self.maxRadius = maxRadius

		self.visionRadius = visionRadius
		self.laodingRadus = laodingRadus

		self.anchor = anchor

		self.trees = []
		self.treeReserve = []


	def fillReserve(self, n):
		for i in range(n):
			self.treeReserve.append(Tree())


	def start(self):
		base.taskMgr.add(self.genTree, "mapGenTask")
		base.taskMgr.add(self.purge, "purgeTask")


	def genTree(self, Task):
		for _ in range(10):
			# Pick a random point inside the loading zone, using gaussian disribution for radius to spawn trees near the player more frequently
			theta = uniform(0, 2*math.pi)
			r = gauss(self.visionRadius, (self.laodingRadus - self.visionRadius)/3.5)
			r = r if r > self.visionRadius else self.visionRadius + (self.visionRadius - r)
	
			x = r*math.cos(theta) + self.anchor.getX()
			y = r*math.sin(theta) + self.anchor.getY()
	
			valid = True
			maxPosibleRadius = self.maxRadius
	
			# Check weather its possible to spawn a tree in
			for clearing in Map.clearings:
				r = clearing.maxRadiusForCircleAt(x,y)
				if r < self.minRadius:
					valid = False
					break
				else:
					maxPosibleRadius = min(maxPosibleRadius, r)
	
			# Spawn tree
			if valid:
				if len(self.treeReserve) > 0:
					r = maxPosibleRadius 
					tree = self.treeReserve.pop() #Tree((x,y,0), r)
					tree.setPosition(x,y,0)
					tree.setClearingRadius(r)
					Map.registerClearing(tree.clearing)
					tree.load()
					self.trees.append(tree)
				else:
					print("Empty tree reserve for map generation")

		return Task.cont

		

	def purge(self, task):
		#Remove trees outside loading zone
		for tree in self.trees:
			if dist(self.anchor.getX(), self.anchor.getY(), tree.getX(), tree.getY()) > self.laodingRadus:
				Map.unregisterClearing(tree.clearing)
				tree.unload()
				self.trees.remove(tree)
				self.treeReserve.insert(0, tree)

		return Task.cont


def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

