import math
from enum import Enum
from random import uniform, gauss
from direct.task import Task

import util
from trees.tree import Tree
from map.location import NoiseTreeSpot

class Map:

	class State(Enum):
		traveling = 0
		visiting = 1

	clearings = []
	locations = []
	currentLocation = None
	state = State.traveling

	visionDistance = 2500
	loadingDistance = 3200


	def init():
		Map.locations.append(NoiseTreeSpot())
		Map.locations[0].setPos(0, 6000, 0)
		Map.locations[0].build()
		Map.locations[0].load()
		Map.currentLocation = Map.locations[0]

		Map.registerClearing(Map.currentLocation.clearing)

	def registerClearing(clearing):
		Map.clearings.append(clearing)

	def unregisterClearing(clearing):
		Map.clearings.remove(clearing)


	def update(info):
		Map.currentLocation.update(info)
		player = info['player']


		distToLoc = util.distObj(player, Map.currentLocation)


		if Map.state == Map.State.visiting:
			
			if distToLoc > Map.visionDistance + Map.currentLocation.clearing.r:
				Map.currentLocation.unload()
				Map.unregisterClearing(Map.currentLocation.clearing)

				#Move to next location
				Map.currentLocation.load()
				Map.currentLocation.setPos(0, Map.currentLocation.spawnDistance, 0, player.getNode())
				Map.registerClearing(Map.currentLocation.clearing)
				Map.state = Map.State.traveling
				print('now traveling')

		elif Map.state == Map.State.traveling:
			if distToLoc > Map.loadingDistance + Map.currentLocation.clearing.r:
				Map.currentLocation.setPos(0, distToLoc, 0, player.getNode())

			if distToLoc < Map.currentLocation.clearing.r:
				Map.state = Map.State.visiting
				print('now visiting')


		else:
			print(Map.state)








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


		#Check which clearings are inside loading zone
		clearingsInLoadingZone = []
		for clearing in Map.clearings:
			if util.dist(self.anchor.getX(), self.anchor.getY(), clearing.x, clearing.y) + clearing.r >= self.visionRadius:
				clearingsInLoadingZone.append(clearing)

		#print('{}, {}'.format(len(Map.clearings), len(clearingsInLoadingZone)))

		for _ in range(3):
			# Pick a random point inside the loading zone, using gaussian disribution for radius to spawn trees near the player more frequently
			theta = uniform(0, 2*math.pi)
			r = gauss(self.visionRadius, (self.laodingRadus - self.visionRadius)/3.5)
			r = r if r > self.visionRadius else self.visionRadius + (self.visionRadius - r)
	
			x = r*math.cos(theta) + self.anchor.getX()
			y = r*math.sin(theta) + self.anchor.getY()
	
			valid = True
			maxPosibleRadius = self.maxRadius
	
			# Check weather its possible to spawn a tree in
			for clearing in Map.clearings: #clearingsInLoadingZone:
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
			if util.dist(self.anchor.getX(), self.anchor.getY(), tree.getX(), tree.getY()) > self.laodingRadus:
				Map.unregisterClearing(tree.clearing)
				tree.unload()
				self.trees.remove(tree)
				self.treeReserve.insert(0, tree)

		return Task.cont


