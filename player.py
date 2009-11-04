import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task

class Player(DirectObject):
    def __init__(self):
       self._keymap = {
               'forward'   : 0,
               'backwards' : 0,
               'right'     : 0,
               'left'      : 0,
       }
       self._load_models()
       self._load_lights()
       self._configure_camera()
       self._setup_actions()

    def _load_models(self):
        self._model = Actor("player")
        self._model.reparentTo(render)

    def _load_lights(self):
        self._headlight = Spotlight('player-headlight')
        self._headlight.setColor((1,1,1,1))
        #self._headlight.showFrustum()
        headlight_path = self._model.attachNewNode(self._headlight)
        headlight_path.setZ(300)
        render.setLight(headlight_path)

    def _configure_camera(self):
        camera.reparentTo(self._model)
        camera.setPos(0, 1200, 1800)
        camera.setHpr(0, -15, 0)

    def _setup_actions(self):
        self.accept("arrow_up", self._set_key, ["forward", 1])
        self.accept("arrow_up-up", self._set_key, ["forward", 0])
        self.accept("arrow_down", self._set_key, ["reverse", 1])
        self.accept("arrow_down-up", self._set_key, ["reverse", 0])
        self.accept("arrow_left", self._set_key, ["left", 1])
        self.accept("arrow_left-up", self._set_key, ["left", 0])
        self.accept("arrow_right", self._set_key, ["right", 1])
        self.accept("arrow_right-up", self._set_key, ["right", 0])

    def _set_key(self, key, value):
        self._keymap[key] = value
