import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task

import math


class Player(DirectObject):
    def __init__(self):
       self._keymap = {
               'forward' : 0,
               'reverse' : 0,
               'right'   : 0,
               'left'    : 0,
       }
       self._camera_pos = (0, -50, 20)
       self._load_models()
       self._load_lights()
       self._configure_camera()
       self._setup_actions()
       self._setup_tasks()
       self._setup_collisions()

    def _load_models(self):
        self._model = Actor("player")
        self._model.reparentTo(render)
        self._model.setPos(0, 0, 5)
        self._model.setScale(.1)

    def _load_lights(self):
        headlight = Spotlight('player-headlight')
        headlight.setColor((1, 1, 1, 1))
        headlight.setLens(PerspectiveLens())
        headlight.getLens().setFov(30, 15)
        headlight.setAttenuation(Vec3(1, 0, 0))
        headlight.setExponent(.5)
        headlight_path = self._model.attachNewNode(headlight)
        headlight_path.setPos(0, 0, 0)
        headlight_path.setHpr(0, 0, 0)
        render.setLight(headlight_path)

    def _configure_camera(self):
        camera.reparentTo(self._model)
        camera.setPos(self._camera_pos[0], self._camera_pos[1], self._camera_pos[2])
        camera.lookAt(self._model)

    def _setup_actions(self):
        self.accept("arrow_up", self._set_key, ["forward", 1])
        self.accept("arrow_up-up", self._set_key, ["forward", 0])
        self.accept("arrow_down", self._set_key, ["reverse", 1])
        self.accept("arrow_down-up", self._set_key, ["reverse", 0])
        self.accept("arrow_left", self._set_key, ["left", 1])
        self.accept("arrow_left-up", self._set_key, ["left", 0])
        self.accept("arrow_right", self._set_key, ["right", 1])
        self.accept("arrow_right-up", self._set_key, ["right", 0])

    def _setup_tasks(self):
        self._prev_move_time = 0
        taskMgr.add(self._task_move, "player-task-move")

    def _setup_collisions(self):
        self._coll_trav = CollisionTraverser()
        self._gnd_handler = CollisionHandlerQueue()
        # Nose collision
        self._gnd_ray = CollisionRay()
        self._gnd_ray.setOrigin(0, 10, 20)
        self._gnd_ray.setDirection(0, 0, -1)
        self._gnd_coll = CollisionNode('collision-ground-front')
        self._gnd_coll.addSolid(self._gnd_ray)
        self._gnd_coll.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path = self._model.attachNewNode(self._gnd_coll)
        #self._gnd_coll_path.show()
        self._coll_trav.addCollider(self._gnd_coll_path, self._gnd_handler)
        # Rear collision
        self._gnd_ray_rear = CollisionRay()
        self._gnd_ray_rear.setOrigin(0, -10, 20)
        self._gnd_ray_rear.setDirection(0, 0, -1)
        self._gnd_coll_rear = CollisionNode('collision-ground-back')
        self._gnd_coll_rear.addSolid(self._gnd_ray_rear)
        self._gnd_coll_rear.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll_rear.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path_rear = self._model.attachNewNode(self._gnd_coll_rear)
        #self._gnd_coll_path_rear.show()
        self._coll_trav.addCollider(self._gnd_coll_path_rear, self._gnd_handler)
        # Camera collision
        self._gnd_ray_cam = CollisionRay()
        self._gnd_ray_cam.setOrigin(self._camera_pos[0], self._camera_pos[1], 20)
        self._gnd_ray_cam.setDirection(0, 0, -1)
        self._gnd_coll_cam = CollisionNode('collision-ground-cam')
        self._gnd_coll_cam.addSolid(self._gnd_ray_cam)
        self._gnd_coll_cam.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll_cam.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path_cam = self._model.attachNewNode(self._gnd_coll_cam)
        #self._gnd_coll_path_cam.show()
        self._coll_trav.addCollider(self._gnd_coll_path_cam, self._gnd_handler)

    def _set_key(self, key, value):
        self._keymap[key] = value

    def _task_move(self, task):
        et = task.time - self._prev_move_time
        rotation_rate = 100
        walk_rate = 10
        # Get current values
        rotation = self._model.getH()
        pos_x = self._model.getX()
        pos_y = self._model.getY()
        pos = self._model.getPos()
        # Rotate the player
        dr = et * rotation_rate
        rotation += self._keymap['left'] * dr
        rotation -= self._keymap['right'] * dr
        # Move the player
        rotation_rad = deg2Rad(rotation)
        dx = et * walk_rate * -math.sin(rotation_rad)
        dy = et * walk_rate * math.cos(rotation_rad)
        pos_x += self._keymap['forward'] * dx
        pos_y += self._keymap['forward'] * dy
        pos_x -= self._keymap['reverse'] * dx
        pos_y -= self._keymap['reverse'] * dy
        # Save back to the model
        self._model.setH(rotation)
        self._model.setX(pos_x)
        self._model.setY(pos_y)
        self._prev_move_time = task.time

        self._coll_trav.traverse(render)

        entries = []
        for i in range(self._gnd_handler.getNumEntries()):
            entries.append(self._gnd_handler.getEntry(i))
        entries.sort(lambda x, y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if entries:
            if entries[0].getIntoNode().getName() == "terrain":
                self._model.setZ(entries[0].getSurfacePoint(render).getZ())
            else:
                self._model.setPos(pos)
        return Task.cont
