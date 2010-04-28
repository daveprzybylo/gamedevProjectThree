import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import *    #basic Panda modules
from direct.showbase.DirectObject import DirectObject  #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import *  #for compound intervals
from direct.task import Task         #for update fuctions
import sys, math, random

class World(DirectObject): #necessary to accept events
    #initializer
    def __init__(self):
        #turn off default mouse control, otherwise camera is not repositionable
        base.disableMouse()
        #camera.setPosHpr(0, -15, 7, 0, -15, 0)
        render.setShaderAuto()
        self.keyMap = {"left":0, "right":0, "forward":0, "reverse":0}
        self.loadModels()
        camera.reparentTo(self.panda)
        #Move camera Up
        camera.setZ(2000)
        #Move camera Back
        camera.setY(3600)
        #Turn camera 180 degrees
        camera.setH(180)
        #Tilt the camera down
        camera.setP(-15)
        self.setupLights()
        self.setupCollisions()
        taskMgr.add(self.move, "moveTask")
        self.prevtime = 0
        self.isMoving = False
        #self.eatSound = loader.loadSfx("something.wav")
        #self.music = loader.loadMusic("music.mp3")
        #self.accept("escape", sys.exit) #message name, function to call, list of arguments
        #"mouse1" is the event when the left mouse button is clicked
        #other interval methods: loop(), pause(), resuem(), finish()
        #start() can take arguments: start(starttime, endtime, playrate)
        self.accept("arrow_up", self.setKey, ["forward", 1])
        self.accept("arrow_left", self.setKey, ["left", 1])
        self.accept("arrow_right", self.setKey, ["right", 1])
        self.accept("arrow_up-up", self.setKey, ["forward", 0])
        self.accept("arrow_left-up", self.setKey, ["left", 0])
        self.accept("arrow_right-up", self.setKey, ["right", 0])
        self.accept("arrow_down", self.setKey, ["reverse", 1])
        self.accept("arrow_down-up", self.setKey, ["reverse", 0])
        self.accept("ate-smiley", self.test_eat)
        #startPos = self.env.find("**/start_point").getPos()
        #self.panda.setPos(startPos)
        self.panda.setZ(100)

    def setKey(self, key, value):
        self.keyMap[key] = value

    def loadModels(self):
        """loads initial models into the world"""
        self.panda = Actor("panda-model", {"walk":"panda-walk4", "eat":"panda-eat"})
        self.panda.reparentTo(render)
        self.panda.setScale(.0005)
        self.panda.setH(180)
        self.env = loader.loadModel("models/world")
        self.env.reparentTo(render)
        self.env.setScale(.25)
        self.env.setPos(0,0,0)
        #load targets
        self.targets = []
        for i in range(5):
            target = loader.loadModel("smiley")
            target.setScale(.5)
            target.setPos(random.uniform(-20, 20), i, 2)
            target.reparentTo(render)
            self.targets.append(target)

    def setupLights(self):
        """Loads initial lighting"""
        self.dirLight = DirectionalLight("dirLight")
        self.dirLight.setColor((.6, .6, .6, 1)) #alpha is largely irrelevant
        #create a NodePath, and attach it directly in the scene
        self.dirLightNP = render.attachNewNode(self.dirLight)
        self.dirLightNP.setHpr(0, -26, 0)
        #the NP that calls setLight is what is illuminated by the light
        #use clearLight() to turn it off
        #render.setLight(self.dirLightNP)

        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor((.25, .25, .25, 1))
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        render.setLight(self.ambientLightNP)

        self.headLight = Spotlight('headLight')
        self.headLight.setColor((1,1,1,1))
        self.headLight.setLens(PerspectiveLens())
        self.headLight.getLens().setFov(45,15)
        self.headLight.setAttenuation(Vec3(1.0,0.0,0.0))
        self.headLight.setExponent(.5)
        self.headLightNP = self.panda.attachNewNode(self.headLight)
        self.headLightNP.setH(180)
        self.headLightNP.setZ(100)
        self.headLightNP.setP(-20)

        #Display the cone
        self.headLight.showFrustum()
        render.setLight(self.headLightNP)

    def move(self, task):
        """Compound interval for walking"""
        self.cTrav.traverse(render)
        startpos = self.panda.getPos()
        elapsed = task.time - self.prevtime
        #camera.lookAt(self.panda)
        if self.keyMap["left"]:
            self.panda.setH(self.panda.getH() + elapsed * 100)
        if self.keyMap["right"]:
            self.panda.setH(self.panda.getH() - elapsed * 100)
        if self.keyMap["forward"]:
            dist = .1
            angle = deg2Rad(self.panda.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.panda.setPos(self.panda.getX() + dx, self.panda.getY() + dy, 0)
        if self.keyMap["reverse"]:
            dist = -.1
            angle = deg2Rad(self.panda.getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.panda.setPos(self.panda.getX() + dx, self.panda.getY() + dy, 0)
        if self.keyMap["left"] or self.keyMap["right"] or self.keyMap["forward"]:
            if self.isMoving == False:
                self.isMoving = True
                self.panda.loop("walk")
        else:
            if self.isMoving:
                self.panda.stop()
                self.panda.pose("walk", 4)
                self.isMoving = False
        self.prevtime = task.time

        entries = []
        for i in range(self.ralphGroundHandler.getNumEntries()):
            entry = self.ralphGroundHandler.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.panda.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.panda.setPos(startpos)

        entries=[]
        for i in range(self.ralphGroundHandlerRear.getNumEntries()):
            entry = self.ralphGroundHandlerRear.getEntry(i)
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.panda.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.panda.setPos(startpos)
        return Task.cont

    def setupCollisions(self):
        self.cHandler = CollisionHandlerEvent()
        #sets the pattern for the event sent on collision
        # "%in" is substituted with the name of the into object
        self.cHandler.setInPattern("ate-%in")
        #makes a collision traverser and sets it to the default
        base.cTrav = CollisionTraverser()

        #cSphere = CollisionSphere((0,0,0), 500) #panda is scaled way down
        #cNode = CollisionNode("panda")
        #cNode.addSolid(cSphere)
        #cNode.setIntoCollideMask(BitMask32.allOff())
        #cNodePath = self.panda.attachNewNode(cNode)
        #cNodePath.show()
        #base.cTrav.addCollider(cNodePath, self.cHandler)
            #cNodePath.show()

        self.cTrav = CollisionTraverser()
        self.ralphGroundRay = CollisionRay()
        self.ralphGroundRay.setOrigin(0,-250,1000)
        self.ralphGroundRay.setDirection(0,0,-1)
        self.ralphGroundCol = CollisionNode('ralphRay')
        self.ralphGroundCol.addSolid(self.ralphGroundRay)
        self.ralphGroundCol.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.ralphGroundColNp = self.panda.attachNewNode(self.ralphGroundCol)
        #self.ralphGroundColNp.show()
        self.ralphGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNp, self.ralphGroundHandler)

        self.ralphGroundRayRear = CollisionRay()
        self.ralphGroundRayRear.setOrigin(0,250,1000)
        self.ralphGroundRayRear.setDirection(0,0,-1)
        self.ralphGroundColRear = CollisionNode('ralphRay')
        self.ralphGroundColRear.addSolid(self.ralphGroundRayRear)
        self.ralphGroundColRear.setFromCollideMask(BitMask32.bit(0))
        self.ralphGroundColRear.setIntoCollideMask(BitMask32.allOff())
        self.ralphGroundColNpRear = self.panda.attachNewNode(self.ralphGroundColRear)
        #self.ralphGroundColNp.show()
        self.ralphGroundHandlerRear = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphGroundColNpRear, self.ralphGroundHandlerRear)

    def eat(self, cEntry):
        """handles panda eating a smiley"""
        self.targets.remove(cEntry.getIntoNodePath().getParent())
        cEntry.getIntoNodePath().getParent().remove()

    def test_eat(self, cEntry):
        self.eat(cEntry)
        if len(self.targets) <= 0:
            sys.exit()

w = World()
run()
