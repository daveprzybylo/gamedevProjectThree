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
        #self._camera_pos = (0, -75, 20)
        self._camera_pos = (0,-10,2)
        self._cam_min_dist = 2
        self._dir = 0
        self._coll_dist = 10
        self._coll_dist_h = 3
        self._scale = .1

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
        self._model.setScale(self._scale)
        self._floater = NodePath(PandaNode("floater"))
        self._floater.reparentTo(render)
        self._floater.setPos(self._model.getPos())

    def _load_lights(self):
        self._headlight = Spotlight('player-headlight')
        self._headlight.setColor((1, 1, 1, 1))
        self._headlight.setLens(PerspectiveLens())
        self._headlight.getLens().setFov(30, 15)
        self._headlight.setAttenuation(Vec3(1, 0, 0))
        self._headlight.setExponent(.5)
        self._headlight_path = self._model.attachNewNode(self._headlight)
        self._headlight_path.setPos(0, 0, 0)
        self._headlight_path.setHpr(0, 0, 0)
        render.setLight(self._headlight_path)
        self._headlight_on = True

    def _configure_camera(self):
        camera.reparentTo(self._floater)
        #camera.reparentTo(self._model)
        camera.setPos(self._camera_pos[0], self._camera_pos[1], self._camera_pos[2])
        camera.lookAt(self._floater)
        #camera.lookAt(self._model)

    def _setup_actions(self):
        self.accept("arrow_up", self._set_key, ["forward", 1])
        self.accept("arrow_up-up", self._set_key, ["forward", 0])
        self.accept("arrow_down", self._set_key, ["reverse", 1])
        self.accept("arrow_down-up", self._set_key, ["reverse", 0])
        self.accept("arrow_left", self._set_key, ["left", 1])
        self.accept("arrow_left-up", self._set_key, ["left", 0])
        self.accept("arrow_right", self._set_key, ["right", 1])
        self.accept("arrow_right-up", self._set_key, ["right", 0])
        self.accept('f',self._toggle_headlight)

    def _toggle_headlight(self):
        if self._headlight_on:
            render.clearLight(self._headlight_path)
            self._headlight_on = False
        else:
            render.setLight(self._headlight_path)
            self._headlight_on = True

    def _setup_tasks(self):
        self._prev_move_time = 0
        taskMgr.add(self._task_move, "player-task-move")

    def _setup_collisions(self):
        self._coll_trav = CollisionTraverser()
        # Front collision
        self._gnd_handler_front = CollisionHandlerQueue()
        self._gnd_ray_front = CollisionRay()
        self._gnd_ray_front.setOrigin(0, self._coll_dist, 20)
        self._gnd_ray_front.setDirection(0, 0, -1)
        self._gnd_coll_front = CollisionNode('collision-ground-front')
        self._gnd_coll_front.addSolid(self._gnd_ray_front)
        self._gnd_coll_front.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll_front.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path_front = self._model.attachNewNode(self._gnd_coll_front)
        #self._gnd_coll_path_front.show()
        self._coll_trav.addCollider(self._gnd_coll_path_front, self._gnd_handler_front)
        # Back collision
        self._gnd_handler_back = CollisionHandlerQueue()
        self._gnd_ray_back = CollisionRay()
        self._gnd_ray_back.setOrigin(0, -self._coll_dist, 20)
        self._gnd_ray_back.setDirection(0, 0, -1)
        self._gnd_coll_back = CollisionNode('collision-ground-back')
        self._gnd_coll_back.addSolid(self._gnd_ray_back)
        self._gnd_coll_back.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll_back.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path_back = self._model.attachNewNode(self._gnd_coll_back)
        #self._gnd_coll_path_back.show()
        self._coll_trav.addCollider(self._gnd_coll_path_back, self._gnd_handler_back)
        # Left collision
        self._gnd_handler_left = CollisionHandlerQueue()
        self._gnd_ray_left = CollisionRay()
        self._gnd_ray_left.setOrigin(-self._coll_dist_h, 0, 20)
        self._gnd_ray_left.setDirection(0, 0, -1)
        self._gnd_coll_left = CollisionNode('collision-ground-left')
        self._gnd_coll_left.addSolid(self._gnd_ray_left)
        self._gnd_coll_left.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll_left.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path_left = self._model.attachNewNode(self._gnd_coll_left)
        #self._gnd_coll_path_left.show()
        self._coll_trav.addCollider(self._gnd_coll_path_left, self._gnd_handler_left)
        # Right collision
        self._gnd_handler_right = CollisionHandlerQueue()
        self._gnd_ray_right = CollisionRay()
        self._gnd_ray_right.setOrigin(self._coll_dist_h, 0, 20)
        self._gnd_ray_right.setDirection(0, 0, -1)
        self._gnd_coll_right = CollisionNode('collision-ground-right')
        self._gnd_coll_right.addSolid(self._gnd_ray_right)
        self._gnd_coll_right.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll_right.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path_right = self._model.attachNewNode(self._gnd_coll_right)
        #self._gnd_coll_path_right.show()
        self._coll_trav.addCollider(self._gnd_coll_path_right, self._gnd_handler_right)
        # Camera collision
        self._gnd_handler_cam = CollisionHandlerQueue()
        self._gnd_ray_cam = CollisionRay()
        self._gnd_ray_cam.setOrigin(self._camera_pos[0], self._camera_pos[1], 20)
        self._gnd_ray_cam.setDirection(0, 0, -1)
        self._gnd_coll_cam = CollisionNode('collision-ground-cam')
        self._gnd_coll_cam.addSolid(self._gnd_ray_cam)
        self._gnd_coll_cam.setFromCollideMask(BitMask32.bit(0))
        self._gnd_coll_cam.setIntoCollideMask(BitMask32.allOff())
        self._gnd_coll_path_cam = self._model.attachNewNode(self._gnd_coll_cam)
        #self._gnd_coll_path_cam.show()
        self._coll_trav.addCollider(self._gnd_coll_path_cam, self._gnd_handler_cam)

    def _set_key(self, key, value):
        self._keymap[key] = value

    def _task_move(self, task):
        et = task.time - self._prev_move_time
        rotation_rate = 100
        walk_rate = 10
        cam_rate = .1
        cam_turn = 1.3
        #cam_turn = 10
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

        self._coll_trav.traverse(render)

        entries_front = []
        entries_back = []
        entries_left = []
        entries_right = []
        for i in range(self._gnd_handler_front.getNumEntries()):
            entries_front.append(self._gnd_handler_front.getEntry(i))
        for i in range(self._gnd_handler_back.getNumEntries()):
            entries_back.append(self._gnd_handler_back.getEntry(i))
        for i in range(self._gnd_handler_left.getNumEntries()):
            entries_left.append(self._gnd_handler_left.getEntry(i))
        for i in range(self._gnd_handler_right.getNumEntries()):
            entries_right.append(self._gnd_handler_right.getEntry(i))
        entries_all = entries_front + entries_back + entries_left + entries_right
        srt = lambda x, y: cmp(y.getSurfacePoint(render).getZ(),
                               x.getSurfacePoint(render).getZ())
        entries_front.sort(srt)
        entries_back.sort(srt)
        entries_left.sort(srt)
        entries_right.sort(srt)
        if entries_all:
            is_valid = lambda x: x and x[0].getIntoNode().getName() == "terrain"
            if is_valid(entries_front) and is_valid(entries_back) and is_valid(entries_left) and is_valid(entries_right):
                f = entries_front[0].getSurfacePoint(render).getZ()
                b = entries_back[0].getSurfacePoint(render).getZ()
                l = entries_left[0].getSurfacePoint(render).getZ()
                r = entries_right[0].getSurfacePoint(render).getZ()
                z = (f + b) / 2
                self._model.setZ(z)
                self._model.setP(rad2Deg(math.atan2(f - z, self._coll_dist * self._scale)))
                self._model.setR(rad2Deg(math.atan2(l - z, self._coll_dist_h * self._scale)))
            else:
                self._model.setPos(pos)
        self._floater.setPos(self._model.getPos())
        self._floater.setH(self._model.getH())

        entries_cam = []
        for i in range(self._gnd_handler_cam.getNumEntries()):
            entries_cam.append(self._gnd_handler_cam.getEntry(i))
        entries_cam = filter(lambda x: x.getIntoNode().getName() == "terrain", entries_cam)
        cam_z = self._camera_pos[2]
        if entries_cam:
            cam_z = max(cam_z, entries_cam[0].getSurfacePoint(render).getZ() + self._cam_min_dist)
        ival = None
        if self._keymap['left']:
            if not self._dir == -1:
                self._dir = -1
                ival = camera.posHprInterval(cam_rate,
                        (-cam_turn, camera.getY(), cam_z),
                        (-cam_turn, camera.getP(), camera.getR()))
        elif self._keymap['right']:
            if not self._dir == 1:
                self._dir = 1
                ival = camera.posHprInterval(cam_rate,
                        (cam_turn, camera.getY(), cam_z),
                        (cam_turn, camera.getP(), camera.getR()))
        else:
            if not self._dir == 0:
                self._dir = 0
                ival = camera.posHprInterval(cam_rate / 2,
                        (0, camera.getY(), cam_z),
                        (0, camera.getP(), camera.getR()))
        if ival:
            ival.start()

        self._prev_move_time = task.time
        return Task.cont
