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

import math
import os
import random
import sys


class Enemy(DirectObject):
    def __init__(self, pos):
        self._load_models(pos)
        self._setup_collisions()
        self._setup_tasks()

    def _load_models(self, pos):
        self._model = Actor(os.path.join('models', 'enemy'),
                {'enemove' : os.path.join('models', 'enemy_walk')})
        self._model.setPos(pos[0], pos[1], pos[2])
        self._model.reparentTo(render)

    def _setup_collisions(self):
        self._coll_trav = CollisionTraverser()
        # Ground collision
        self._ground_handler = CollisionHandlerQueue()
        self._ground_ray = CollisionRay()
        self._ground_ray.setOrigin(0, 0, 1)
        self._ground_ray.setDirection(0, 0, -1)
        self._ground_coll = CollisionNode('collision-ground')
        self._ground_coll.addSolid(self._ground_ray)
        self._ground_coll.setFromCollideMask(BitMask32.bit(0))
        self._ground_coll.setIntoCollideMask(BitMask32.allOff())
        self._ground_coll_path = self._model.attachNewNode(self._ground_coll)
        #self._ground_coll_path.show()
        self._coll_trav.addCollider(self._ground_coll_path, self._ground_handler)
        # Sight collision
        self._sight_handler = CollisionHandlerQueue()
        self._sight_ray = CollisionRay()
        self._sight_ray.setOrigin(-2, 0, 1)
        self._sight_ray.setDirection(0, -1, 0)
        self._sight_coll = CollisionNode('collision-sight')
        self._sight_coll.addSolid(self._sight_ray)
        self._sight_coll.setFromCollideMask(BitMask32.bit(5))
        self._sight_coll.setIntoCollideMask(BitMask32.allOff())
        self._sight_coll_path = self._model.attachNewNode(self._sight_coll)
        #self._sight_coll_path.show()
        self._coll_trav.addCollider(self._sight_coll_path, self._sight_handler)
        # Sight collision (High)
        self._sight_handler_hi = CollisionHandlerQueue()
        self._sight_ray_hi = CollisionRay()
        self._sight_ray_hi.setOrigin(-2, 0, 1)
        self._sight_ray_hi.setDirection(0, -1, .075)
        self._sight_coll_hi = CollisionNode('collision-sight-hi')
        self._sight_coll_hi.addSolid(self._sight_ray_hi)
        self._sight_coll_hi.setFromCollideMask(BitMask32.bit(5))
        self._sight_coll_hi.setIntoCollideMask(BitMask32.allOff())
        self._sight_coll_hi_path = self._model.attachNewNode(self._sight_coll_hi)
        #self._sight_coll_hi_path.show()
        self._coll_trav.addCollider(self._sight_coll_hi_path, self._sight_handler_hi)
        # Sight collision (Low)
        self._sight_handler_lo = CollisionHandlerQueue()
        self._sight_ray_lo = CollisionRay()
        self._sight_ray_lo.setOrigin(-2, 0, 1)
        self._sight_ray_lo.setDirection(0, -1, -.075)
        self._sight_coll_lo = CollisionNode('collision-sight-lo')
        self._sight_coll_lo.addSolid(self._sight_ray_lo)
        self._sight_coll_lo.setFromCollideMask(BitMask32.bit(5))
        self._sight_coll_lo.setIntoCollideMask(BitMask32.allOff())
        self._sight_coll_lo_path = self._model.attachNewNode(self._sight_coll_lo)
        #self._sight_coll_lo_path.show()
        self._coll_trav.addCollider(self._sight_coll_lo_path, self._sight_handler_lo)
        # Player collision
        self._player_handler = CollisionHandlerQueue()
        self._player = CollisionSphere(0, 0, 0, 10)
        self._player_coll = CollisionNode('collision-with-player')
        self._player_coll.addSolid(self._player)
        self._player_coll.setFromCollideMask(BitMask32.bit(0))
        self._player_coll.setIntoCollideMask(BitMask32.bit(7))
        self._player_coll_path = self._model.attachNewNode(self._player_coll)
        self._player_coll_path.show()
        self._coll_trav.addCollider(self._player_coll_path, self._player_handler)

    def _setup_tasks(self):
        self._prev_time = 0
        taskMgr.add(self._move, "task-enemy-move")

    def _move(self, task):
        et = task.time - self._prev_time
        rotation_rate = 100
        walk_rate = 25

        # Get current values
        rotation = self._model.getH()
        pos_x = self._model.getX()
        pos_y = self._model.getY()
        pos = self._model.getPos()

        self._coll_trav.traverse(render)

        self._sight_handler.sortEntries()
        self._sight_handler_hi.sortEntries()
        self._sight_handler_lo.sortEntries()
        if self._sight_handler.getNumEntries() and self._sight_handler.getEntry(0).getIntoNode().getName() == 'collision-player-sphere' or \
            self._sight_handler_hi.getNumEntries() and self._sight_handler_hi.getEntry(0).getIntoNode().getName() == 'collision-player-sphere' or \
            self._sight_handler_lo.getNumEntries() and self._sight_handler_lo.getEntry(0).getIntoNode().getName() == 'collision-player-sphere':
            rotation_rad = deg2Rad(rotation)
            dx = et * walk_rate * math.sin(rotation_rad)
            dy = et * walk_rate * -math.cos(rotation_rad)
            pos_x += dx
            pos_y += dy
        else:
            rotation += et * rotation_rate

        # Save back to the model
        self._model.setH(rotation)
        self._model.setX(pos_x)
        self._model.setY(pos_y)

        self.pos = self._model.getPos()

        entries = []
        for i in range(self._ground_handler.getNumEntries()):
            entries.append(self._ground_handler.getEntry(i))

        entries.sort(lambda x, y: cmp(y.getSurfacePoint(render).getZ(),
                                      x.getSurfacePoint(render).getZ()))
        if len(entries) > 0 and entries[0].getIntoNode().getName().find('terrain') != -1:
            self._model.setZ(entries[0].getSurfacePoint(render).getZ() + .2)
        else:
            self._model.setPos(self.pos)

        self._prev_time = task.time
        return Task.cont
