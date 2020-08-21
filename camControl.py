from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import WindowProperties
from panda3d.core import KeyboardButton
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

class CamControl(DirectObject):

	def __init__(self, showBase):

		self.lastX = None
		self.lastY = None
		self.heading = 0
		self.pitch = 0

		self.baseSpeed = 200
		self.fwSpeed = 0
		self.sideSpeed = 0

		base.disableMouse()
		props = WindowProperties()
		props.setCursorHidden(True)
		props.setMouseMode(WindowProperties.M_relative)
		base.win.requestProperties(props)

		showBase.taskMgr.add(self.mouseListenerTask, "mouseListenerTask")
		showBase.taskMgr.add(self.walkTask, "walkTask")



		self.controlMap = {"left": False, "right": False, "forward": False, "backward": False}

		self.accept("w", self.setControl, ["forward", True])
		self.accept("a", self.setControl, ["left", True])
		self.accept("s", self.setControl, ["backward", True])
		self.accept("d", self.setControl, ["right", True])
		self.accept("w-up", self.setControl, ["forward", False])
		self.accept("a-up", self.setControl, ["left", False])
		self.accept("s-up", self.setControl, ["backward", False])
		self.accept("d-up", self.setControl, ["right", False])
		self.accept("arrow_up", self.setControl, ["forward", True])
		self.accept("arrow_left", self.setControl, ["left", True])
		self.accept("arrow_down", self.setControl, ["backward", True])
		self.accept("arrow_right", self.setControl, ["right", True])
		self.accept("arrow_up-up", self.setControl, ["forward", False])
		self.accept("arrow_left-up", self.setControl, ["left", False])
		self.accept("arrow_down-up", self.setControl, ["backward", False])
		self.accept("arrow_right-up", self.setControl, ["right", False])



	def setControl(self, key, val):
		self.controlMap[key] = val



	def mouseListenerTask(self, task):
		mw = base.mouseWatcherNode
		if mw.hasMouse():
			x, y = mw.getMouseX(), mw.getMouseY()

			if self.lastX != None:
				dx = self.lastX - x
				dy = self.lastY - y
				self.heading = self.heading + dx * 20
				self.pitch = self.pitch - dy * 20
				base.cam.setHpr(self.heading, self.pitch, 0)

			self.lastX = x
			self.lastY = y
		return Task.cont



	def walkTask(self, task):
		self.forwadSpeed = 0
		self.sideSpeed = 0

		if self.controlMap['forward']:
			self.forwadSpeed = self.baseSpeed

		if self.controlMap['backward']:
			self.forwadSpeed = -self.baseSpeed

		if self.controlMap['right']:
			self.sideSpeed = self.baseSpeed

		if self.controlMap['left']:
			self.sideSpeed = -self.baseSpeed

		y_delta = self.forwadSpeed * globalClock.get_dt()
		x_delta = self.sideSpeed * globalClock.get_dt()

		base.cam.setPos(base.cam, x_delta, y_delta, 0)
		base.cam.setZ(0)
		
		#currentY = base.cam.getY()
		#base.cam.setY(currentY +y_delta)
		return Task.cont