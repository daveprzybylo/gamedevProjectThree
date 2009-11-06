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
       self._setup_tasks()
       self._setup_collisions()

    def _load_models(self):
        self._model = Actor("player")
        self._model.reparentTo(render)

    def _load_lights(self):
        self._headlight = Spotlight('player-headlight')
        self._headlight.setColor((1,1,1,1))
        #self._headlight.showFrustum()
        self._headlight.setLens(PerspectiveLens())
        self._headlight.getLens().setFov(45,15)
        self._headlight.setAttenuation(Vec3(1,0,0))
        self._headlight.setExponent(.5)
        headlight_path = self._model.attachNewNode(self._headlight)
        headlight_path.setPos(0, 0, 100)
        headlight_path.setHpr(0, -20, 0)
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

    def _setup_tasks(self):
        self._prev_move_time = 0
        taskMgr.add(self._task_move, "player-task-move")

    def _setup_collisions(self):
        cTrav = CollisionTraverser()
        groundRay = CollisionRay()
        groundRay.setOrigin(0,-250,1000)
        groundRay.setDirection(0,0,-1)
        groundCol = CollisionNode('groundRay')
        groundCol.addSolid(groundRay)
        groundCol.setFromCollideMask(BitMask32.bit(0))
        groundCol.setIntoCollideMask(BitMask32.allOff())
        groundColNp = self._model.attachNewNode(groundCol)
        #groundColNp.show()
        self.groundHandler = CollisionHandlerQueue()
        cTrav.addCollider(groundColNp, self.groundHandler)

    def _set_key(self, key, value):
        self._keymap[key] = value

    def _task_move(self, task):
        et = task.time - self._prev_move_time
        rotation_rate = 100
        walk_rate = .1
        # Get current values
        rotation = self._model.getH()
        pos_x = self._model.getX()
        pos_y = self._model.getY()
        pos = self._model.getPos()
        # Rotate the player
        rotation += self._keymap['left'] * rotation_rate * et
        rotation -= self._keymap['right'] * rotation_rate * et
        # Move the player
        rotation_deg = deg2Rad(rotation)
        dx = walk_rate * math.sin(angle)
        dy = walk_rate * -math.cos(angle)
        pos_x += self._keymap['forward'] * dx
        pos_y += self._keymap['reverse'] * dy
        # Save back to the model
        self._model.setH(rotation)
        self._model.setX(pos_x)
        self._model.setY(pos_y)
        self._prev_move_time = task.time

        entries = []
        for i in range(self.groundHandler.getNumEntries()):
            entries.append(self.groundHandler.getEntry(i))
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if entries and (entries[0].getIntoNode().getName() == "terrain"):
            self._model.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self._model.setPos(pos)
        return Task.cont
