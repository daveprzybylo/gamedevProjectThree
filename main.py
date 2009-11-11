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
from pandac.PandaModules import loadPrcFileData 
loadPrcFileData( '', 'notify-level fatal' )

import player
import enemy

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
        self.env = loader.loadModel(os.path.join("models","environment"))
        self.env.reparentTo(render)
        self.env.setPos(0, 0, 0)
        for i in range(5):
            newenemy= enemy.enemy(i, self.player._coll_trav)
            self.enemylist.append(enemy)

    def _setup_lights(self):
        ambient = AmbientLight("light-ambient")
        ambient.setColor((.13, .13, .13, 1))
        ambient_path = render.attachNewNode(ambient)
        render.setLight(ambient_path)


def start_game():
    b.destroy()
    c.destroy()
    d.destroy()
    textObject.destroy()


if __name__ == '__main__':
    bk_text = "Satan's Space Sanctuary"
    font = loader.loadFont(os.path.join("fonts","arial.ttf"))
    font.setPixelsPerUnit(200)
    textObject = OnscreenText(text=bk_text, font=font, pos = (0, 0.7),
                              scale=0.2, fg=(1, 1, 1, 1),
                              mayChange=0)
    b = DirectButton(text="Start Game", text_font=font, clickSound=None,
                     command=start_game, text_fg=(0, 0, 0, 1), scale=.1,
                     pos=(0, 0, -.5), relief=None)
    b.setTransparency(1)
    d = DirectButton(text="Quit", text_font=font, clickSound=None,
                     command=sys.exit, text_fg=(0, 0, 0, 1), scale=.1,
                     pos=(0, 0, -.62), relief=None)
    d.setTransparency(1)
    c = OnscreenImage(parent=render2d, image=os.path.join("models","background.png"))
    ambientSound = loader.loadSfx(os.path.join("sounds", "Ambient wind.mp3"))
    ambientSound.play()
    ambientSound.setLoop(True)

    w = World()
    run()
