import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import * 
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task

import player

import sys
import os


game_started = False

class World(DirectObject):
    def __init__(self):
        base.disableMouse()
        render.setShaderAuto()
        self._setup_models()
        self._setup_lights()
        #self.music = loader.loadMusic("music.mp3")
        self.accept("escape", sys.exit)
        self.accept("enter", start_game)


    def _setup_models(self):
        self.player = player.Player()
        self.env = loader.loadModel(os.path.join('models','world'))
        self.env.reparentTo(render)
        self.env.setPos(0, 0, 0)

    def _setup_lights(self):
        ambient = AmbientLight("light-ambient")
        ambient.setColor((.25, .25, .25, 1))
        ambient_path = render.attachNewNode(ambient)
        render.setLight(ambient_path)


def start_game():
    b.destroy()
    c.destroy()
    d.destroy()
    textObject.destroy()


if __name__ == '__main__':
    bk_text = "Game Menu"
    font = loader.loadFont('arial.ttf')
    font.setPixelsPerUnit(200)
    textObject = OnscreenText(text=bk_text, font=font, pos=(0, 0, .5),
                              scale=0.2, fg=(1, 1, 1, 1),
                              align=TextNode.ACenter, mayChange=1)
    b = DirectButton(text="Start Game", text_font=font, clickSound=None,
                     command=start_game, text_fg=(1, 1, 1, 1), scale=.1,
                     pos=(0, 0, -.5), relief=None)
    b.setTransparency(1)
    d = DirectButton(text="Quit", text_font=font, clickSound=None,
                     command=sys.exit, text_fg=(1, 1, 1, 1), scale=.1,
                     pos=(0, 0, -.62), relief=None)
    d.setTransparency(1)
    c = OnscreenImage(parent=render2d, image="background.png")

    w = World()
    run()
