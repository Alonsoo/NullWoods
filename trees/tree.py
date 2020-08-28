import math
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs
from panda3d.core import GeomNode
from panda3d.core import NodePath
from opensimplex import OpenSimplex
from map.clearing import ClearingCircle
import random

class Tree:

	def __init__(self, origin = None):
		self.branchCount = 0
		self.clearing = None
		self.maxDepth = 9
		#self.noise = OpenSimplex()
		self.lineSegs = []

		self.treeSource = self.branch(100, 0, 0)
		self.geomNode = GeomNode('tree node')
		self.nodePath = NodePath(self.geomNode)

		self.draw()

		if origin != None:
			self.setPosition(origin[0], origin[1], origin[2])


	def setClearingRadius(self, r):
		if self.clearing == None:
			self.clearing = ClearingCircle(self.getX(), self.getY(), r)
		else:
			self.clearing.r = r

	def setPosition(self, x, y, z):
		self.nodePath.setPos(x,y,z)
		#self.position = pos
		if self.clearing != None:
			self.clearing.x = self.getX()
			self.clearing.y = self.getY()


	def getX(self):
		return self.nodePath.getX() #self.position[0]

	def getY(self):
		return self.nodePath.getY() #self.position[1]

	def getZ(self):
		return self.nodePath.getZ() #self.position[2]



	def branch(self, length, theta, phi, depth = 0):
		if depth > self.maxDepth: #length < self.minLength:
			return None

		branches = []

		for _ in range(2):
			newTheta = 0.0
			newphi = 0.0
			newLength = 0.0

			newTheta = random.uniform(0, 2*math.pi)
			newPhi = random.gauss(math.pi/4, 0.4) #random.uniform(0, math.pi/2)
	
			newLength = length * min(random.gauss(0.75, 0.1), 0.95)
	
			branches.append(self.branch(newLength, newTheta, newPhi, depth + 1))


		branchId = self.branchCount
		self.branchCount += 1

		return Branch(branchId, length, theta, phi, depth, branches)



	def drawBranch(self, branch, origin, info):

		if len(self.lineSegs) <= branch.depth:
			lineSeg = LineSegs('')
			lineSeg.setThickness(branch.length / 10) # make depth dependent instead of branch length dependent
			self.lineSegs.append(lineSeg)


		line = self.lineSegs[branch.depth]
		color = Tree.map(branch.length, 100, 0, 0, .45)
		line.setColor(color, color, color)

		x1, y1, z1 = origin

		phi, theta = self.getBranchAngles(branch, info)

		z2 = z1 + branch.length * math.cos(phi)
		pLength = branch.length * math.sin(phi)
		x2 = x1 + pLength * math.cos(theta)
		y2 = y1 + pLength * math.sin(theta)

		dest = (x2, y2, z2)

		line.moveTo(x1, y1, z1)
		line.drawTo(x2, y2, z2)

		for child in branch.children:
			if child != None:
				self.drawBranch(child, dest, info)


	def getBranchAngles(self, branch, info):
		return (branch.phi, branch.theta)


	def draw(self, info = None):
		self.geomNode.removeAllGeoms()

		self.drawBranch(self.treeSource, (0,0,0), info)

		for lineSeg in self.lineSegs:
			lineSeg.create(self.geomNode, True)

	def update(self, info):
		self.draw(info)


	def load(self):
		self.nodePath.reparentTo(render)

	def unload(self):
		self.nodePath.detachNode()


	def cleanup(self):
		self.nodePath.removeNode()
		self.nodePath = None



	@staticmethod
	def map(val, start1, stop1, start2, stop2):
		return ((val - start1) * (stop2 - start2)/(stop1 - start1)) + start2





class Branch:

	 def __init__(self, id, length, theta, phi, depth, children = []):
	 	self.id = id
	 	self.length = length
	 	self.theta = theta
	 	self.phi = phi
	 	self.depth = depth
	 	self.children = children


