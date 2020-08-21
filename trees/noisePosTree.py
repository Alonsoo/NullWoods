import math
from trees.tree import Tree



class NoisePosTree(Tree):

	def __init__(self, origin):
		Tree.__init__(self, origin)


	def getBranchAngles(self, branch, info):
		phi, theta = branch.phi, branch.theta
		if branch.depth != 0:
			phi += self.noise.noise2d(x = branch.id + info.x * branch.depth, y = branch.id + info.y * branch.depth)
			theta += self.noise.noise2d(x = branch.id + info.x * branch.depth, y = branch.id + info.y * branch.depth + 10)
		return (phi, theta)