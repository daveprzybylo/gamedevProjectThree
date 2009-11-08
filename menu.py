from direct.filter.CommonFilters import CommonFilters 
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import * 
from direct.gui.DirectGui import *
loadPrcFileData("", "framebuffer-multisample 1")
import direct.directbase.DirectStart
 
# Add some text

bk_text = "Game Menu"
textObject = OnscreenText(text = bk_text,  pos = (0,0,.5), 
scale = 0.2,fg=(1,1,1,1),align=TextNode.ACenter,mayChange=1)


 
# Callback function to set  text
def setText():
        bk_text = "Game Started"
        textObject.setText(bk_text)
 
# Add button
b = DirectButton(text="Start Game", clickSound = None, command=setText, text_fg=(1,1,1,1), scale=.15, pos = (0,0,-.5), relief=None)
b.setTransparency(1)
c = OnscreenImage(parent=render2d, image="background.png")
# Run the tutorial
run()