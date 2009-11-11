from pandac.PandaModules import loadPrcFileData
loadPrcFileData('', 'window-title Satan\'s Space Sanctuary')
loadPrcFileData('', 'notify-level fatal')
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
        self._setup_actions()
        self.artifact_count = 0

    def got_artifact(self,cEntry):
        if self.artifact_count > 1:
            print 'You got Satans artifact, yay!'
        else:
            self.artifact_count += 1

    def _setup_models(self):
        self.player = player.Player()
        self.env = loader.loadModel(os.path.join("models", "environment"))
        self.env.reparentTo(render)
        self.env.setPos(0, 0, 0)
        self.enemylist = []
        # Tutorial Enemy
        self.enemylist.append(enemy.Enemy((0, 0, 100)))
        # Wave 1
        self.enemylist.append(enemy.Enemy((-47.4, 123.6, 13.9)))
        self.enemylist.append(enemy.Enemy((-30.6, 125.4, 16.4)))
        # Wave 2
        self.enemylist.append(enemy.Enemy((-176.6, 222.2, 25)))
        self.enemylist.append(enemy.Enemy((-177.704, 232.321, 25)))
        self.enemylist.append(enemy.Enemy((-175.9, 239.482, 28)))
        # Wave 3
        self.enemylist.append(enemy.Enemy((-333.3, 209.9, 35)))
        self.enemylist.append(enemy.Enemy((-340.9, 216.5, 31)))
        self.enemylist.append(enemy.Enemy((-346.6, 224.8, 35)))
        self.enemylist.append(enemy.Enemy((-359.1, 215.4, 34)))
        self.enemylist.append(enemy.Enemy((-355.9, 198.7, 36)))

        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.setInPattern("artifact_gotten")

        self.artifact = loader.loadModel('panda')
        self.artifact.setScale(.5)
        self.artifact.setPos(-290,9,275)
        self.artifact.reparentTo(render)

        cSphere = CollisionSphere(0,0,0,10)
        cNode = CollisionNode("artifact")
        cNode.addSolid(cSphere)
        cNode.setIntoCollideMask(BitMask32.bit(3))

        cNodePath = self.artifact.attachNewNode(cNode)
        base.cTrav.addCollider(cNodePath, self.cHandler)

    def _setup_lights(self):
        ambient = AmbientLight("light-ambient")
        ambient.setColor((.13, .13, .13, 1))
        ambient_path = render.attachNewNode(ambient)
        render.setLight(ambient_path)

    def _setup_actions(self):
        self.accept("escape", sys.exit)
        self.accept("enter", start_game)
        self.accept('artifact_gotten', self.got_artifact)


def start_game():
    b.destroy()
    c.destroy()
    d.destroy()
    textObject.destroy()


if __name__ == '__main__':
    bk_text = "Satan's Space Sanctuary"
    font = loader.loadFont(os.path.join("fonts", "arial.ttf"))
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
    c = OnscreenImage(parent=render2d, image=os.path.join("models", "background.png"))
    sound_ambient = loader.loadSfx(os.path.join("sounds", "ambient-wind.mp3"))
    sound_ambient.play()
    sound_ambient.setLoop(True)

    w = World()
    run()
