import math
from trees.tree import Tree

class NoiseTree(Tree):

	def __init__(self, origin):
		Tree.__init__(self, origin)


	def getBranchAngles(self, branch, info):
		phi, theta = branch.phi, branch.theta
		if branch.depth != 0:
			phi += self.noise.noise2d(x = branch.id + info.t/12 * branch.depth, y = 0)
			theta += self.noise.noise2d(x = branch.id + info.t/12 * branch.depth, y = 10)
		return (phi, theta)