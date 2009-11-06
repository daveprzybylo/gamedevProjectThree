import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task

import player

import sys


class World(DirectObject):
    def __init__(self):
        base.disableMouse()
        render.setShaderAuto()
        self._setup_models()
        self._setup_lights()
        #self.music = loader.loadMusic("music.mp3")
        self.accept("escape", sys.exit)

    def _setup_models(self):
        self.player = player.Player()
        self.env = loader.loadModel("models/world")
        self.env.reparentTo(render)
        self.env.setPos(0, 0, 0)

    def _setup_lights(self):
        ambient = AmbientLight("light-ambient")
        ambient.setColor((.25, .25, .25, 1))
        ambient_path = render.attachNewNode(ambient)
        render.setLight(ambient_path)


if __name__ == '__main__':
    w = World()
    run()
