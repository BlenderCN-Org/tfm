#############################################################################
#                 OFFICE ENVIRONMENT GENERATION CODE                        #
#                     PEDRO MIGUEL LUZON MARTINEZ                           #
#############################################################################

import bmesh, bpy, random, sys, copy
import bpy
import random
import sys
import os
import copy
import time
sys.path.append(".")

from lsystem import Grammar
from materials import Materials
from proceduralSetting import ProceduralGeometry


def clearScene():
    bpy.context.scene.layers[0] = True
    rem = [item.name for item in bpy.data.objects]
    for r in rem:
        bpy.data.objects[r].select = True
    bpy.ops.object.delete()
    bpy.context.scene.update()
def save():
    filename = 'office_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.blend'
    bpy.ops.wm.save_as_mainfile(filepath=filename, check_existing=False, copy=True)
    print("Office saved as %s", filename)
    print("Now you can generate another environment again!\n")

class Office:
    def __init__(self, ogF):
        self.officeGrammarFile = ogF
        self.officeGrammar = Grammar(self.officeGrammarFile)
        self.proceduralMachine = ProceduralGeometry(self.officeGrammar.roomsL, self.officeGrammar.roomsR, self.officeGrammar.noise,
                                                    self.officeGrammar.meeting, self.officeGrammar.bathroom)

    def makeOffice(self, sub):
        officeGrammarStr = self.officeGrammar.deriveString(sub)
        self.proceduralMachine.generateGeometry(officeGrammarStr)



#Procedurally generate office environment
clearScene() #Remove everything
Materials().generateNewMaterials() #Generate materials
office = Office("grammar.grammar") #Set grammars
office.makeOffice(4) #Start generating office with n (from 1 to 4) levels of detail
save() #saves result in a new blend file
