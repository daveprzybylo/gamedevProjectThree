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

import random

import sys
import os

import math

class enemy(DirectObject):
    def __init__(self, i, cTrav):
        self.cTrav=cTrav
        self._load_models(i)
        self._prev_time=0
        taskMgr.add(self._move, "enemy-task-move")
        self._setupCollisions()
    def _load_models(self,i):
	self.nmy = Actor(os.path.join('models','enemy'), {'enemove' : os.path.join('models','enemy_walk')})

        self.nmy.setScale(1)
        self.nmy.setPos(0, 0, 100)
        self.nmy.reparentTo(render)
        self.pos=self.nmy.getPos()
    def _move(self, task):
        elapsed= task.time - self._prev_time
        foundpanda=0
        sightentries= []
        for i in range(self.enemySightHandler.getNumEntries()):
            entry=self.enemySightHandler.getEntry(i)
            sightentries.append(entry)
            if (sightentries[i].getIntoNode().getName()=="playerSphere"):
                foundpanda=1


        if(foundpanda==0):
            self.nmy.setH(self.nmy.getH() + 5) 
                  
        else:
            
            angle = deg2Rad(self.nmy.getH())
            dist = .5
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.nmy.setPos(self.nmy.getX() + dx, self.nmy.getY() + dy, 0)
        self.startpos=self.nmy.getPos()
        entries=[]
	for i in range(self.enemyGroundHandler.getNumEntries()):
            entry = self.enemyGroundHandler.getEntry(i)
            entries.append(entry)
            
            
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName().find('terrain') != -1):
            self.nmy.setZ(entries[0].getSurfacePoint(render).getZ()+.2)
        else:
            self.nmy.setPos(self.startpos)
        return task.cont

    def _setupCollisions(self):
        
        self.enemyGroundRay = CollisionRay()
        self.enemyGroundRay.setOrigin(0,0,1)
        self.enemyGroundRay.setDirection(0,0,-1)
        self.enemyGroundCol = CollisionNode('enemyRay')
        self.enemyGroundCol.addSolid(self.enemyGroundRay)
        self.enemyGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.enemyGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.enemyGroundColNp = self.nmy.attachNewNode(self.enemyGroundCol)
        #self.enemyGroundColNp.show()
        self.enemyGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.enemyGroundColNp, self.enemyGroundHandler)
        
        self.enemySightRay= CollisionRay()
        self.enemySightRay.setOrigin(-2,0,1)
        self.enemySightRay.setDirection(0,-1,0)
        self.enemySightCol = CollisionNode('enemysightRay')
        self.enemySightCol.addSolid(self.enemySightRay)
        self.enemySightCol.setFromCollideMask(BitMask32.bit(5))
        self.enemySightCol.setIntoCollideMask(BitMask32.allOff())
        self.enemySightColNp = self.nmy.attachNewNode(self.enemySightCol)
        #self.enemySightColNp.show()
        self.enemySightHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.enemySightColNp, self.enemySightHandler)

        self.playersphere= CollisionSphere(0,0,0,10)
        self.playerColsphere = CollisionNode('enemySphere')
        self.playerColsphere.addSolid(self.playersphere)
        self.playerColsphere.setFromCollideMask(BitMask32.bit(0))
        self.playerColsphere.setIntoCollideMask(BitMask32.bit(5))
        self.playerColNPsphere = self.nmy.attachNewNode(self.playerColsphere)
        self.playerColNPsphere.show()

