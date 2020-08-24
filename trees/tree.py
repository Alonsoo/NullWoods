import math
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs
from panda3d.core import GeomNode
from panda3d.core import NodePath
from opensimplex import OpenSimplex
from map.clearing import ClearingCircle
import random

class Tree:

	def __init__(self, origin, clearingR):
		self.branchCount = 0
		self.position = origin
		self.clearing = ClearingCircle(self.position[0], self.position[1], clearingR)
		self.angleMode = 'random'
		self.lengthScale = -1 # set to -1 for randomized scales
		self.minLength = 10
		self.noise = OpenSimplex()
		self.lineSegs = []

		self.treeSource = self.branch(100, 0, 0)


	def getX(self):
		return self.position[0]

	def getY(self):
		return self.position[1]

	def getZ(self):
		return self.position[2]



	def branch(self, length, theta, phi, depth = 0):
		if length < self.minLength:
			return None

		branches = []

		for _ in range(2):
			newTheta = 0.0
			newphi = 0.0
			newLength = 0.0
	
			if self.angleMode == 'random':
				newTheta = random.uniform(0, 2*math.pi)
				newPhi = random.gauss(math.pi/4, 0.4) #random.uniform(0, math.pi/2)
	
			if self.lengthScale == -1:
				newLength = length * min(random.gauss(0.75, 0.1), 0.95)
			else:
				newLength = length * self.lengthScale

			branches.append(self.branch(newLength, newTheta, newPhi, depth + 1))


		branchId = self.branchCount
		self.branchCount += 1

		return Branch(branchId, length, theta, phi, depth, branches)



	def drawBranch(self, branch, origin, info):

		if len(self.lineSegs) <= branch.depth:
			lineSeg = LineSegs('')
			lineSeg.setThickness(branch.length / 10) # make depth dependent instead of branch length dependent?
			self.lineSegs.append(lineSeg)


		line = self.lineSegs[branch.depth] #LineSegs('')
		color = Tree.map(branch.length, 100, 0, 0, .45)
		line.setColor(color, color, color)
		#line.setThickness(branch.length / 10)

		x1, y1, z1 = origin

		phi, theta = self.getBranchAngles(branch, info)

		z2 = z1 + branch.length * math.cos(phi)
		pLength = branch.length * math.sin(phi)
		x2 = x1 + pLength * math.cos(theta)
		y2 = y1 + pLength * math.sin(theta)

		dest = (x2, y2, z2)

		line.moveTo(x1, y1, z1)
		line.drawTo(x2, y2, z2)
		#line.create(self.geomNode, True)

		for child in branch.children:
			if child != None:
				self.drawBranch(child, dest, info)


	def getBranchAngles(self, branch, info):
		return (branch.phi, branch.theta)



	def create(self):
		self.geomNode = GeomNode('tree node')
		self.update()
		return NodePath(self.geomNode)


	def update(self, info = None):
		self.geomNode.removeAllGeoms()

		self.drawBranch(self.treeSource, (0,0,0), info)

		for lineSeg in self.lineSegs:
			lineSeg.create(self.geomNode, True)

		#TODO: checar bien que onda con esto
		self.clearing.x = self.position[0]
		self.clearing.y = self.position[1]


	def load(self):
		self.nodePath = self.create()
		self.nodePath.reparentTo(render)
		self.nodePath.setPos(self.position)

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


