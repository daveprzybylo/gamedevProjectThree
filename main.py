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

    def got_artifact(self, cEntry):
        #print cEntry
        if cEntry.getFromNode().getName() == 'artifact' and cEntry.getIntoNode().getName().find('player') != -1:
            print 'You Win!'

    def _setup_models(self):
        self.player = player.Player()
        self.env = loader.loadModel(os.path.join("models", "environment"))
        self.env.reparentTo(render)
        self.env.setPos(0, 0, 0)
        self.enemylist = []
        self._wave_one()
        taskMgr.add(self._task_checkpoint, "world-task-checkpoint")
        
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.setInPattern("artifact_gotten")
        
        self.artifact = loader.loadModel(os.path.join('models','artifact'))
        self.artifact.setPos(-290,9,283)
        self.artifact.reparentTo(render)
        
        cSphere = CollisionSphere(0,0,0,10)
        cNode = CollisionNode("artifact")
        cNode.addSolid(cSphere)
        cNode.setIntoCollideMask(BitMask32.bit(3))
    
        cNodePath = self.artifact.attachNewNode(cNode)
        #cNodePath.show()
        self.player._coll_trav.addCollider(cNodePath, self.cHandler)
        

    def _wave_one(self):
        self.wave=1
        
        # Tutorial Enemy
        self.enemylist.append(enemy.Enemy((0, 0, 10)))
        # Wave 1
        self.enemylist.append(enemy.Enemy((-47.4, 123.6, 13.9)))
        self.enemylist.append(enemy.Enemy((-30.6, 125.4, 16.4)))
    def _wave_two(self):
        print "1"
        self.wave=2
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        # Wave 2
        self.enemylist.append(enemy.Enemy((-176.6, 222.2, 25)))
        self.enemylist.append(enemy.Enemy((-177.704, 232.321, 25)))
        self.enemylist.append(enemy.Enemy((-175.9, 239.482, 28)))
    def _wave_three(self):
        print "2"
        self.wave=3
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        # Wave 3
        self.enemylist.append(enemy.Enemy((-333.3, 209.9, 35)))
        self.enemylist.append(enemy.Enemy((-340.9, 216.5, 31)))
        self.enemylist.append(enemy.Enemy((-346.6, 224.8, 35)))
        self.enemylist.append(enemy.Enemy((-359.1, 215.4, 34)))
        self.enemylist.append(enemy.Enemy((-355.9, 198.7, 36)))
    def _wave_four(self):
        print "3"
        self.wave=4
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        # Wave 4
        self.enemylist.append(enemy.Enemy((-438.3, 98.5, 43.5)))
        self.enemylist.append(enemy.Enemy((-443.2, 98.6, 40.5)))
        self.enemylist.append(enemy.Enemy((-471.3, 47.1, 45.8)))
        self.enemylist.append(enemy.Enemy((-462.0, 45.2, 41.7)))
    def _wave_five(self):
        self.wave=5
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        # Wave 5
        self.enemylist.append(enemy.Enemy((-469.4, -51.2, 49.9)))
        self.enemylist.append(enemy.Enemy((-447.1, -53.9, 53.4)))
        self.enemylist.append(enemy.Enemy((-440.7, -110.4, 52.7)))
        self.enemylist.append(enemy.Enemy((-430.7, -113.3, 53.2)))
    def _wave_six(self):
        self.wave=6
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        # Wave 6
        self.enemylist.append(enemy.Enemy((-246.0, -204.9, 70.0)))
        self.enemylist.append(enemy.Enemy((-207.1, -199.3, 71.7)))
        self.enemylist.append(enemy.Enemy((-188.3, -194.4, 72.7)))
    def _wave_seven(self):
        self.wave=7
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        
        # Wave 7
        self.enemylist.append(enemy.Enemy((-107.9, -153.4, 82.6)))
        self.enemylist.append(enemy.Enemy((-94.1, -139.5, 84.5)))
        self.enemylist.append(enemy.Enemy((-78.9, -118.3, 84.6)))
    def _wave_eight(self):
        self.wave=8
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        # Wave 8
        self.enemylist.append(enemy.Enemy((-61.4, -14.2, 92.8)))
        self.enemylist.append(enemy.Enemy((-64.3, 24.7, 98.9)))
        self.enemylist.append(enemy.Enemy((-71.8, 63.2, 99.6)))
    def _wave_nine(self):
        self.wave=9
        for i in range(len(self.enemylist)):
            self.enemylist[i]._model.delete()
            self.enemylist[i].dead=True
        self.enemylist = []
        # Wave 9
        self.enemylist.append(enemy.Enemy((-145.6, 159.2, 108.9)))
        self.enemylist.append(enemy.Enemy((-203.6, 185.9, 118.8)))
        self.enemylist.append(enemy.Enemy((-248.6, 186.0, 127.3)))
        # Wave 10

    def _setup_lights(self):
        ambient = AmbientLight("light-ambient")
        ambient.setColor((.13, .13, .13, 1))
        ambient_path = render.attachNewNode(ambient)
        render.setLight(ambient_path)

    def _setup_actions(self):
        self.accept("escape", sys.exit)
        self.accept("enter", start_game)
        self.accept('artifact_gotten', self.got_artifact)

    def _task_checkpoint(self, task):
        if self.player._model.getZ()  > 20 and self.wave==1:
            self._wave_two()
        if self.player._model.getZ()  > 25.8 and self.wave==2:
            self._wave_three()
        if self.player._model.getZ() > 37  and self.wave==3:
            self._wave_four()
        if self.player._model.getZ() > 42.9  and self.wave==4:
            self._wave_five()
        if self.player._model.getZ() > 60  and self.wave==5:
            self._wave_six()
        if self.player._model.getZ() > 75  and self.wave==6:
            self._wave_seven()
        if self.player._model.getZ() > 82.1  and self.wave==7:
            self._wave_eight()
        if self.player._model.getZ() > 105  and self.wave==8:
            self._wave_nine()
        return Task.cont

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
