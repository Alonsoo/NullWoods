from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs
from panda3d.core import NodePath
from panda3d.core import Camera
from panda3d.core import OrthographicLens
from panda3d.core import Fog
from direct.task import Task
from pandac.PandaModules import *

from trees.tree import Tree
from trees.noiseTree import NoiseTree
from trees.noisePosTree import NoisePosTree
from camControl import CamControl
from map.map import Map
from map.map import MapTreeGen

import types
import sys
import pdb

ConfigVariableBool('fullscreen').setValue(1)

class ForestApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

		self.setSceneGraphAnalyzerMeter(False)
		self.setFrameRateMeter(True)

		self.accept('escape', sys.exit)

		base.camLens.setFov(90)
		base.camLens.setFar(2000)
		base.setBackgroundColor(255,255,255)

		base.cam.setPos(0, 0, 80)


		myFog = Fog("Fog Name")
		myFog.setMode(Fog.MExponentialSquared)
		myFog.setColor(255,255, 255)
		myFog.setExpDensity(0.001)
		self.render.setFog(myFog)

		self.camControl = CamControl(self)

		Map.init()

		mapGen = MapTreeGen(100, 100, 2500, 3000, self.camControl)
		mapGen.fillReserve(700)
		mapGen.start()

		base.taskMgr.add(self.updateMap, "mapUpdateTask")
		

		"""cols, rows = 10, 100
		self.trees = []

		for col in range(cols):
			for row in range(rows):
				tree = Tree((col*300 - 450, row*200 - 1000, 0))
				treeNP = tree.create()
				tree.draw()
				treeNP.reparentTo(self.render)
				self.trees.append(tree)"""

		#self.tree = NoisePosTree((0, 300, 0))
		#self.tree.create().reparentTo(render)

		#base.taskMgr.add(self.updateTrees, "updateTreesTask")
		#base.taskMgr.add(self.dolly, "dollyTask")

	def updateMap(self, task):
		info = {'t': task.time,
				'player': self.camControl}
		Map.update(info)
		return Task.cont


	def updateTrees(self, task):
		"""for tree in self.trees:
			info = types.SimpleNamespace()
			info.t = task.time
			info.x = base.cam.getX()/1000
			info.y = base.cam.getY()/1000
			tree.draw(info)
		return Task.cont"""

		info = types.SimpleNamespace()
		info.t = task.time
		info.x = base.cam.getX()/1000
		info.y = base.cam.getY()/1000
		self.tree.draw(info)
		return Task.cont


	def dolly(self, task):
		base.camLens.setFov(base.cam.getY()/30 + 40)
		base.cam.setR(base.cam.getY()/30)
		return Task.cont


app = ForestApp()
app.run()