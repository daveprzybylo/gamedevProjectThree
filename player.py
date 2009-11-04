import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task

class Player(DirectObject):
    def __init__(self):
       self.keymap = {
               'up'    : 0,
               'down'  : 0,
               'right' : 0,
               'left'  : 0,
       }
       self._load_models()
       self._load_lights()
       self._configure_camera()
       self._setup_actions()

    def _load_models(self):
        pass

    def _load_lights(self):
        pass

    def _configure_camera(self):
        camera.reparentTo(self.model)
        camera.setPos(0, 1200, 1800)
        camera.setHpr(180, -15, 0)

    def _setup_actions(self):
        pass
