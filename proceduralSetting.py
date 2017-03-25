#############################################################################
#                 Procedural room generator code                            #
#############################################################################

from math import sin,cos,pi
from copy import deepcopy
import random
import bpy
import bmesh
import os
import math
import sys
from elements import Elements


class ProceduralGeometry(object):
   commands={}   

   ### Bounds defined as [(top-left corner), (top-right corner), (bottom-left corner), (bottom-right corner)] ###




   def __init__(self, roomsUp, roomsDown, noiseList, meeting, bathroom):
      self.context = []
      self.firstLayer = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False)
      self.secondLayer = (False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,False, False, False, False)
      self.officeSize = (random.uniform(30, 33) * 0.35, random.uniform(33, 45) * 0.35, random.uniform(20, 22) * 0.35) #(length, width, height)
      if meeting == 1:
         self.meetingSize = (random.uniform(50, 60) * 0.35, self.officeSize[1], self.officeSize[2])
      else:
         self.meetingSize = (0,0,0)
      if bathroom == 1:
         self.bathroomSize = (random.uniform(20, 30) * 0.35, self.officeSize[1], self.officeSize[2])
      else:
         self.bathroomSize = (0,0,0)
      self.corridorWidth = random.uniform(10, 15)
      self.totalSurface = ()
      self.lastSurface = []

      ### rate of division of the initial space between meeting and working areas ###
      ### #0.5 : same areas; <0.5 : meeting area > working area; >0.5 : working area > meeting area ###
      self.divisionRate = random.uniform(0.45, 0.55)
      self.divisionRate = 0.5
      print(self.divisionRate)
      ### Bounds defined as [(top-left corner), (top-right corner), (bottom-left corner), (bottom-right corner)] ###
      self.workBounds = []
      self.currentBounds = []
      self.previousBounds = []
      self.lastDesk = []

      self.roomNumberUpOriginal = roomsUp
      self.roomNumberUpLeft = roomsUp
      self.roomNumberDownOriginal = roomsDown
      self.roomNumberDownLeft = roomsDown
      self.noises = noiseList

      self.generatedList = []
      self.completedTasks = []
      self.roomsCounter = 0
      self.upsideDown = False

      self.initializeSurface()


   def mapAndBakeTexture(self):
      print("Preparing wood texture for Blender game engine.")

      bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, layers=self.firstLayer)
      plane = bpy.data.objects['Plane']
      plane.select = True
      bpy.context.scene.objects.active = plane
      plane.data.materials.append(bpy.data.materials[6])
      plane.dimensions = (10, 20, 0)
      bpy.ops.object.mode_set(mode='EDIT')
      bm = bmesh.from_edit_mesh(bpy.context.object.data)
      #bm.faces.ensure_lookup_table()
      for f in bm.faces:
         f.material_index = 0
      plane.data.update()
      if len(bpy.data.images) == 1:
         bpy.ops.image.new(name="WoodTexture", width=1080, height=512)
      bpy.ops.uv.smart_project()
      bpy.context.area.type = 'IMAGE_EDITOR'
      for area in bpy.context.screen.areas:
         if area.type == 'IMAGE_EDITOR':
            area.spaces.active.image = bpy.data.images[1]
      bpy.ops.object.bake_image()
      bpy.ops.image.save_as(filepath="WoodTextureImage.png", check_existing=False, copy=True)
      print("Saving wood texture image.")
      imagepath = os.getcwd() + "/WoodTextureImage.png"
      bpy.ops.image.open(filepath=imagepath)
      plane.data.materials[0] = bpy.data.materials[7]
      plane.data.update()
      bpy.ops.object.bake_image()
      bpy.ops.image.save_as(filepath="WoodTextureImage2.png", check_existing=False, copy=True)
      print("Saving wood2 texture image.")
      imagepath = os.getcwd() + "/WoodTextureImage2.png"
      bpy.ops.image.open(filepath=imagepath)
      plane.data.materials[0] = bpy.data.materials[8]
      plane.data.update()
      bpy.ops.object.bake_image()
      bpy.ops.image.save_as(filepath="WoodTextureImage3.png", check_existing=False, copy=True)
      print("Saving wood3 texture image.")
      imagepath = os.getcwd() + "/WoodTextureImage3.png"
      bpy.ops.image.open(filepath=imagepath)
      bpy.context.area.type = 'TEXT_EDITOR'
      bpy.ops.object.mode_set(mode='OBJECT')
      bpy.ops.object.delete()
      bpy.context.scene.update()
      bpy.context.scene.objects.active = None

      mat = bpy.data.materials['Wood']
      for s in range(len(mat.texture_slots)):
         mat.texture_slots.clear(s)
      tex = bpy.data.textures.new('WoodImage', 'IMAGE')
      slot = mat.texture_slots.add()
      slot.mapping = 'FLAT'
      slot.texture_coords = 'UV'
      slot.uv_layer = 'UVMap'
      slot.use_rgb_to_intensity = False
      slot.use_map_normal = True
      slot.normal_factor = 1.2
      slot.scale = (2.0, 2.0, 2.0)
      tex.image = bpy.data.images[2]
      slot.texture = tex
      mat = bpy.data.materials['Wood2']
      for s in range(len(mat.texture_slots)):
         mat.texture_slots.clear(s)
      tex = bpy.data.textures.new('WoodImage2', 'IMAGE')
      slot = mat.texture_slots.add()
      slot.mapping = 'FLAT'
      slot.texture_coords = 'UV'
      slot.uv_layer = 'UVMap'
      slot.use_rgb_to_intensity = False
      slot.use_map_normal = True
      slot.normal_factor = 1.2
      slot.scale = (2.0, 2.0, 2.0)
      tex.image = bpy.data.images[3]
      slot.texture = tex
      mat = bpy.data.materials['Wood3']
      for s in range(len(mat.texture_slots)):
         mat.texture_slots.clear(s)
      tex = bpy.data.textures.new('WoodImage3', 'IMAGE')
      slot = mat.texture_slots.add()
      slot.mapping = 'FLAT'
      slot.texture_coords = 'UV'
      slot.uv_layer = 'UVMap'
      slot.use_rgb_to_intensity = False
      slot.use_map_normal = True
      slot.normal_factor = 1.2
      slot.scale = (2.0, 2.0, 2.0)
      tex.image = bpy.data.images[4]
      slot.texture = tex
      print("Done.")

   def generateTaskFlow(self):
      b, m = 0, 0
      if self.bathroomSize[0] != 0:
         b = 1
      if self.meetingSize[0] != 0:
         m = 1
      task = -1
      availableTasks = [0, 1 * m, 2 * b]
      side = 0  # side to work with (0->up, 1->down)
      for r in range(self.roomNumberUpOriginal + self.roomNumberDownOriginal + b + m + 1):
         # let's decide randomly what's next (0->office room, 1->meeting, 2->bathroom)
         # if last task was 0 ad there are rooms left, next task will be 0 again
         # completedTasks 1 and 2 cannot be done twice in the same side AND environment
         if side == 0:
            if task == 0 and self.roomNumberUpLeft > 0:
               self.completedTasks.append(0)
            elif len(self.completedTasks) == max(self.roomNumberUpOriginal + b, self.roomNumberUpOriginal + m):
               self.completedTasks.append(-1)
               side = 1
            else:
               while True:
                  r = random.choice(availableTasks)
                  if r not in self.completedTasks:
                     if (r == 1 and 2 not in self.completedTasks) or (r == 2 and 1 not in self.completedTasks):
                        task = r
                        self.completedTasks.append(task)
                        break
                     elif r == 0 and self.roomNumberUpLeft > 0:
                        task = r
                        self.completedTasks.append(task)
                        self.roomNumberUpLeft -= 1
                        break
         if side == 1:
            if task == 0 and self.roomNumberDownLeft > 0:
               self.completedTasks.append(0)
               self.roomNumberDownLeft -= 1
            elif len(self.completedTasks) == self.roomNumberUpOriginal + self.roomNumberDownOriginal + b + m:
               side = -1
            else:
               while True:
                  r = random.choice(availableTasks)
                  if (r not in self.completedTasks):
                     task = r
                     self.completedTasks.append(task)
                     break
                  elif (r == 0 and self.roomNumberDownLeft > 0):
                     task = r
                     self.completedTasks.append(task)
                     self.roomNumberDownLeft -= 1
                     break

   def initializeSurface(self):
      x = max(self.meetingSize[0] + self.roomNumberUpLeft * self.officeSize[0],
              self.meetingSize[0] + self.roomNumberDownLeft * self.officeSize[0],
              self.bathroomSize[0] + self.roomNumberUpLeft * self.officeSize[0],
              self.bathroomSize[0] + self.roomNumberDownLeft * self.officeSize[0])
      y = self.officeSize[1] * 2 + self.corridorWidth
      self.totalSurface = (x,y)
      self.currentBounds = [[0,y], [x,y], [0,0], [x,0]]
      print("Initializing total surface: ", self.currentBounds)
      self.saveContext()

   def initializeNextSurface(self, task, side):
      sizes = [self.officeSize, self.meetingSize, self.bathroomSize]
      print("From last surface: ", self.lastSurface)
      if side == 0:
         if (len(self.lastSurface) == 0):
            self.currentBounds = [self.currentBounds[0],
                                  [sizes[task][0], self.totalSurface[1]],
                                  [0, self.totalSurface[1] - sizes[task][1]],
                                  [sizes[task][0], self.totalSurface[1] - sizes[task][1]]]
            aux = deepcopy(self.currentBounds)
            self.lastSurface = aux
         else:
            self.currentBounds = [self.lastSurface[1],
                                  [self.lastSurface[1][0] + sizes[task][0], self.totalSurface[1]],
                                  self.lastSurface[3],
                                  [self.lastSurface[1][0] + sizes[task][0], self.lastSurface[3][1]]]
            aux = deepcopy(self.currentBounds)
            self.lastSurface = aux
      if side == 1:
         if (len(self.lastSurface) == 0):
            self.currentBounds = [[0, sizes[task][1]],
                                  [sizes[task][0], sizes[task][1]],
                                  [0,0],
                                  [sizes[task][0], 0]]
            aux = deepcopy(self.currentBounds)
            self.lastSurface = aux
         else:
            self.currentBounds = [self.lastSurface[1],
                                  [self.lastSurface[1][0] + sizes[task][0], sizes[task][1]],
                                  self.lastSurface[3],
                                  [self.lastSurface[1][0] + sizes[task][0], 0]]
            aux = deepcopy(self.currentBounds)
            self.lastSurface = aux
      print("Next surface was initialized: ", self.currentBounds)


   def generateFloorAndWalls(self):
      print("Generating room floor and walls. Dimensions: ", self.officeSize)

      #bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=True, location=(0, 0, 0), layers=self.firstLayer)
      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),layers=self.firstLayer)
      room = bpy.data.objects['Cube']
      room.select = True
      bpy.context.scene.objects.active = room
      room.data.materials.append(bpy.data.materials[3])
      room.data.materials.append(bpy.data.materials[5])
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='DESELECT')
      bm = bmesh.from_edit_mesh(bpy.context.object.data)
      #bm.faces.ensure_lookup_table()
      bm.faces[5].select = True
      bpy.ops.mesh.delete(type='FACE')
      #bm.faces.ensure_lookup_table()
      bmesh.update_edit_mesh(bpy.context.edit_object.data, True)
      for f in bm.faces:
         f.material_index = 1
      bm.faces[4].material_index = 0
      room.data.update()
      bpy.ops.mesh.select_all(action='DESELECT')
      bpy.ops.object.mode_set(mode='OBJECT')
      bpy.ops.object.select_all(action='DESELECT')
      bpy.context.scene.objects.active = None
      room.select = False
      #cube = bpy.data.objects[3]
      room.dimensions = (self.currentBounds[1][0] - self.currentBounds[0][0],
                         self.currentBounds[0][1] - self.currentBounds[2][1],
                         self.officeSize[2])
      room.location = ((self.currentBounds[0][0] + self.currentBounds[1][0]) / 2,
                       (self.currentBounds[0][1] + self.currentBounds[2][1]) / 2,
                       self.officeSize[2] / 2.0)

      room.name = 'Room' + str(self.roomsCounter)
      print("Whole room bounds: ", self.currentBounds)

   def generateMeetingBounds(self):
      self.currentBounds[0][1] = ((self.currentBounds[0][1] + self.currentBounds[2][1]) * self.divisionRate)
      self.currentBounds[1][1] = self.currentBounds[0][1]
      print("Defining meeting bounds: ", self.currentBounds)

   def generateWorkBounds(self):
      self.currentBounds[2][1] = ((self.currentBounds[0][1] + self.currentBounds[2][1]) * (1 - self.divisionRate))
      self.currentBounds[3][1] = self.currentBounds[2][1]
      print("Defining working bounds: ", self.currentBounds)

   def generateShelving(self):
      if random.uniform(0, 1) > 0.5:
         self.currentBounds[1][0] -= (self.currentBounds[1][0] - self.currentBounds[0][0]) * 0.75
         self.currentBounds[3][0] -= (self.currentBounds[1][0] - self.currentBounds[0][0]) * 0.75
         orientation = 'L'
      else:
         self.currentBounds[0][0] += (self.currentBounds[1][0] - self.currentBounds[0][0]) * 0.75
         self.currentBounds[2][0] += (self.currentBounds[3][0] - self.currentBounds[2][0]) * 0.75
         orientation = 'R'
      o = Elements().putShelving(self.currentBounds, orientation)
      self.generatedList.append(o)

   def generateMeetingDesk(self):
      print(self.currentBounds)
      print(self.previousBounds)
      if self.previousBounds[0][0] == self.currentBounds[0][0]:
         self.currentBounds[0] = self.previousBounds[1]
         self.currentBounds[2] = self.previousBounds[3]
      else:
         self.currentBounds[1] = self.previousBounds[0]
         self.currentBounds[3] = self.previousBounds[2]
      data = Elements().putMeetingDesk(self.currentBounds)
      self.lastDesk = data[:]
      o = data[-1]
      self.generatedList.append(o)

   def generateLargeMeetingDesk(self):
      data = Elements().putLargeMeetingDesk(self.currentBounds)
      self.lastDesk = data[:]
      o = data[-1]
      self.generatedList.append(o)

   def generateDeskType1(self):
      self.currentBounds[2][1] += (self.currentBounds[0][1] - self.currentBounds[2][1]) * 0.25
      self.currentBounds[3][1] += (self.currentBounds[1][1] - self.currentBounds[3][1]) * 0.25
      data = Elements().putDeskType1(self.currentBounds)
      self.lastDesk = data[:]

      self.currentBounds[0] = [self.lastDesk[1] - (self.lastDesk[5] / 2), self.lastDesk[2] + (self.lastDesk[3] / 2)]
      self.currentBounds[1] = [self.lastDesk[1] + (self.lastDesk[5] / 2), self.lastDesk[2] + (self.lastDesk[3] / 2)]
      self.currentBounds[2] = [self.lastDesk[1] - (self.lastDesk[5] / 2), self.lastDesk[2] - (self.lastDesk[3] / 2)]
      self.currentBounds[3] = [self.lastDesk[1] + (self.lastDesk[5] / 2), self.lastDesk[2] - (self.lastDesk[3] / 2)]
      o = data[-1]
      self.generatedList.append(o)

   def generateDeskType2(self):
      self.currentBounds[2][1] += (self.currentBounds[0][1] - self.currentBounds[2][1]) * 0.25
      self.currentBounds[3][1] += (self.currentBounds[1][1] - self.currentBounds[3][1]) * 0.25
      data = Elements().putDeskType2(self.currentBounds)
      self.lastDesk = data[:]

      self.currentBounds[0] = [self.lastDesk[1] - (self.lastDesk[5] / 2), self.lastDesk[2] + (self.lastDesk[3] / 2)]
      self.currentBounds[1] = [self.lastDesk[1] + (self.lastDesk[5] / 2), self.lastDesk[2] + (self.lastDesk[3] / 2)]
      self.currentBounds[2] = [self.lastDesk[1] - (self.lastDesk[5] / 2), self.lastDesk[2] - (self.lastDesk[3] / 2)]
      self.currentBounds[3] = [self.lastDesk[1] + (self.lastDesk[5] / 2), self.lastDesk[2] - (self.lastDesk[3] / 2)]

      o = data[-1]
      self.generatedList.append(o)

   def generateChairType1(self):
      l = Elements().putChairType1(self.lastDesk, self.currentNoise)
      for o in l:
         self.generatedList.append(o)

   def generateChairType2(self):
      l = Elements().putChairType2(self.lastDesk, self.currentNoise)
      for o in l:
         self.generatedList.append(o)

   def generateBin(self):
      if random.uniform(0, 1) > 0.5:
         orientation = 'R'
         o = Elements().putBin(self.currentBounds[1], self.currentBounds[3], orientation)
      else:
         orientation = 'L'
         o = Elements().putBin(self.currentBounds[0], self.currentBounds[2], orientation)
      self.generatedList.append(o)

   def generateCorkPanel(self):
      if random.uniform(0, 1) > 0.5:
         orientation = 'R'
         o = Elements().putCorkPanel(self.currentBounds[1], self.currentBounds[3], self.officeSize[2], self.currentNoise, orientation)
      else:
         orientation = 'L'
         o = Elements().putCorkPanel(self.currentBounds[0], self.currentBounds[2], self.officeSize[2], self.currentNoise, orientation)
      self.generatedList.append(o)

   def generateProjectorPanel(self):
      if random.uniform(0, 1) > 0.5:
         orientation = 'R'
         o = Elements().putProjectorPanel(self.currentBounds[1], self.currentBounds[3], self.officeSize[2], orientation)
      else:
         orientation = 'L'
         o = Elements().putProjectorPanel(self.currentBounds[0], self.currentBounds[2], self.officeSize[2], orientation)
      self.generatedList.append(o)

   def generateReadingLamp(self):
      l = Elements().putReadingLamp(self.currentBounds, self.lastDesk[6], self.lastDesk[4])
      div = l[0]
      if div > 0.5:
         self.currentBounds[1][0] -= (4 * 0.35)
         self.currentBounds[3][0] -= (4 * 0.35)
      else:
         self.currentBounds[0][0] += (4 * 0.35)
         self.currentBounds[2][0] += (4 * 0.35)
      o = l[1]
      self.generatedList.append(o)

   def generateMonitor(self):
      o = Elements().putMonitor(self.currentBounds, self.lastDesk[6], self.lastDesk[4])
      if self.lastDesk[4] == 90:
         self.currentBounds[0][1] -= (2.6 * 0.35)
         self.currentBounds[1][1] = self.currentBounds[0][1]
      if self.lastDesk[4] == 270:
         self.currentBounds[2][1] += (2.6 * 0.35)
         self.currentBounds[3][1] = self.currentBounds[2][1]
      self.generatedList.append(o)

   def generateKeyboardAndMouse(self):
      l = Elements().putKeyboardAndMouse(self.currentBounds, self.lastDesk[6], self.lastDesk[4])
      for o in l:
         self.generatedList.append(o)

   def generateClothHanger(self):
      o = Elements().putClothHanger(self.currentBounds, self.previousBounds)
      self.generatedList.append(o)

   def saveContext(self):
      print("-- Saving current bounds --")
      aux = deepcopy(self.currentBounds)
      self.context.append(aux)

   def recoverContext(self):
      print("-- Recovering previous bounds --")
      aux = self.context.pop()
      self.previousBounds = deepcopy(self.currentBounds)
      self.currentBounds = deepcopy(aux)

   def generateBathroom(self):
      o1 = Elements().putSink(self.currentBounds)
      o2 = Elements().putToilet(self.currentBounds)
      self.generatedList.append(o1)
      for i in range(len(o2)):
         self.generatedList.append(o2[i])

      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                      layers=self.firstLayer)
      wall1 = bpy.data.objects['Cube']
      wall1.select = True
      bpy.context.scene.objects.active = wall1
      wall1.name = "BathWall_1_" + str(self.roomsCounter)
      wall1.dimensions = ((self.currentBounds[1][0] - self.currentBounds[0][0]), 0.2, self.officeSize[2])
      wall1.location = ((self.currentBounds[1][0] + self.currentBounds[0][0]) / 2,
                        (self.currentBounds[2][1] + (self.currentBounds[0][1] - self.currentBounds[2][1]) * 2.3/3),
                       (self.officeSize[2]) / 2)
      wall1.data.materials.append(bpy.data.materials[5])
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='DESELECT')
      bm = bmesh.from_edit_mesh(bpy.context.object.data)
      # bm.faces.ensure_lookup_table()
      bmesh.update_edit_mesh(bpy.context.edit_object.data, True)
      for f in bm.faces:
         f.material_index = 0
      wall1.data.update()
      bpy.ops.mesh.select_all(action='DESELECT')
      bpy.ops.object.mode_set(mode='OBJECT')
      bpy.context.scene.objects.active = None
      wall1.select = False
      self.generatedList.append(wall1)

      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                      layers=self.firstLayer)
      wall2 = bpy.data.objects['Cube']
      wall2.select = True
      bpy.context.scene.objects.active = wall2
      wall2.name = "BathWall_2_" + str(self.roomsCounter)
      wall2.dimensions = (0.2, (self.currentBounds[0][1] - self.currentBounds[2][1]) * 0.7/3,
                          self.officeSize[2])
      wall2.location = (((self.currentBounds[1][0] - self.currentBounds[0][0]) * 1/3) + self.currentBounds[0][0],
                        (self.currentBounds[0][1] - (self.currentBounds[0][1] - self.currentBounds[2][1]) * 0.7 / 6),
                        (self.officeSize[2]) / 2)
      wall2.data.materials.append(bpy.data.materials[5])
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='DESELECT')
      bm = bmesh.from_edit_mesh(bpy.context.object.data)
      # bm.faces.ensure_lookup_table()
      bmesh.update_edit_mesh(bpy.context.edit_object.data, True)
      for f in bm.faces:
         f.material_index = 0
      wall2.data.update()
      bpy.ops.mesh.select_all(action='DESELECT')
      bpy.ops.object.mode_set(mode='OBJECT')
      bpy.context.scene.objects.active = None
      wall2.select = False
      self.generatedList.append(wall2)

      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                      layers=self.firstLayer)
      wall3 = bpy.data.objects['Cube']
      wall3.select = True
      bpy.context.scene.objects.active = wall3
      wall3.name = "BathWall_3_" + str(self.roomsCounter)
      wall3.dimensions = (0.2, (self.currentBounds[0][1] - self.currentBounds[2][1]) * 0.7 / 3,
                          self.officeSize[2])
      wall3.location = (((self.currentBounds[1][0] - self.currentBounds[0][0]) * 2/3) + self.currentBounds[0][0],
                        (self.currentBounds[0][1] - (self.currentBounds[0][1] - self.currentBounds[2][1]) * 0.7 / 6),
                        (self.officeSize[2]) / 2)
      wall3.data.materials.append(bpy.data.materials[5])
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='DESELECT')
      bm = bmesh.from_edit_mesh(bpy.context.object.data)
      # bm.faces.ensure_lookup_table()
      bmesh.update_edit_mesh(bpy.context.edit_object.data, True)
      for f in bm.faces:
         f.material_index = 0
      wall3.data.update()
      bpy.ops.mesh.select_all(action='DESELECT')
      bpy.ops.object.mode_set(mode='OBJECT')
      bpy.context.scene.objects.active = None
      wall3.select = False
      self.generatedList.append(wall3)

      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                      layers=self.firstLayer)
      door = bpy.data.objects['Cube']
      door.select = True
      bpy.context.scene.objects.active = door
      door.dimensions = ((3 * 0.55), 1, self.officeSize[2] * 0.75)
      door.location = ((self.currentBounds[1][0] + self.currentBounds[0][0]) / 2 + (self.currentBounds[1][0] - self.currentBounds[0][0]) / 3,
                       (self.currentBounds[2][1] + (self.currentBounds[0][1] - self.currentBounds[2][1]) * 2.3 / 3),
                       (self.officeSize[2] * 0.75) / 2)

      door.select = False
      wall1.select = True
      bpy.context.scene.objects.active = wall1
      b1 = wall1.modifiers.new(type='BOOLEAN', name='B1')
      b1.operation = 'DIFFERENCE'
      b1.object = door
      bpy.ops.object.modifier_apply(modifier='B1')
      wall1.select = False
      door.select = True
      bpy.ops.object.delete()
      bpy.context.scene.update()
      door.select = False
      bpy.context.scene.objects.active = None

      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                      layers=self.firstLayer)
      door = bpy.data.objects['Cube']
      door.select = True
      bpy.context.scene.objects.active = door
      door.dimensions = ((3 * 0.55), 1, self.officeSize[2] * 0.75)
      door.location = ((self.currentBounds[1][0] + self.currentBounds[0][0]) / 2 - (
      self.currentBounds[1][0] - self.currentBounds[0][0]) / 3,
                       (self.currentBounds[2][1] + (self.currentBounds[0][1] - self.currentBounds[2][1]) * 2.3 / 3),
                       (self.officeSize[2] * 0.75) / 2)

      door.select = False
      wall1.select = True
      bpy.context.scene.objects.active = wall1
      b1 = wall1.modifiers.new(type='BOOLEAN', name='B2')
      b1.operation = 'DIFFERENCE'
      b1.object = door
      bpy.ops.object.modifier_apply(modifier='B2')
      wall1.select = False
      door.select = True
      bpy.ops.object.delete()
      bpy.context.scene.update()
      door.select = False
      bpy.context.scene.objects.active = None

      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                      layers=self.firstLayer)
      door = bpy.data.objects['Cube']
      door.select = True
      bpy.context.scene.objects.active = door
      door.dimensions = ((3 * 0.55), 1, self.officeSize[2] * 0.75)
      door.location = ((self.currentBounds[1][0] + self.currentBounds[0][0]) / 2,
                       (self.currentBounds[2][1] + (self.currentBounds[0][1] - self.currentBounds[2][1]) * 2.3 / 3),
                       (self.officeSize[2] * 0.75) / 2)

      door.select = False
      wall1.select = True
      bpy.context.scene.objects.active = wall1
      b1 = wall1.modifiers.new(type='BOOLEAN', name='B3')
      b1.operation = 'DIFFERENCE'
      b1.object = door
      bpy.ops.object.modifier_apply(modifier='B3')
      wall1.select = False
      door.select = True
      bpy.ops.object.delete()
      bpy.context.scene.update()
      door.select = False
      bpy.context.scene.objects.active = None

   def generateCorridor(self, meeting, bathroom):
      print("Generating corridor.")
      bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, layers=self.firstLayer)
      corridor = bpy.data.objects['Cube']
      corridor.select = True
      bpy.context.scene.objects.active = corridor
      corridor.name = "Corridor"

      # dimUp, dimDown = 0, 0
      # for i in self.completedTasks:
      #    if i >= max(self.roomNumberUpOriginal + bathroom, self.roomNumberUpOriginal + meeting):
      #       if self.completedTasks[i]
      #    else:
      #       dimUp += 1

      corridor.dimensions = (self.totalSurface[0],
                             self.totalSurface[1] - (self.officeSize[1] * 2), 0.5)
      xMean = ((self.officeSize[1] + 0.8) * (max(self.roomNumberUpOriginal, self.roomNumberDownOriginal) - 1)) / 2
      corridor.location = (self.totalSurface[0] / 2, (self.totalSurface[1] / 2), -0.25)
      corridor.data.materials.append(bpy.data.materials[3])
      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.select_all(action='DESELECT')
      bm = bmesh.from_edit_mesh(bpy.context.object.data)
      #bm.faces.ensure_lookup_table()
      for f in bm.faces:
         f.material_index = 0
      corridor.data.update()
      bpy.ops.mesh.select_all(action='DESELECT')
      bpy.ops.object.mode_set(mode='OBJECT')
      bpy.ops.object.select_all(action='DESELECT')
      bpy.context.scene.objects.active = None
      corridor.select = False

      print("\n--- OFFICE FLOOR GENERATION COMPLETE! ---\n")
      self.mapAndBakeTexture()

   def finishRoom(self):
      print("Applying solidify modifier to the room.")
      roomNumber = 'Room' + str(self.roomsCounter)
      room = bpy.data.objects[roomNumber]
      room.select = True
      bpy.context.scene.objects.active = room
      #self.generatedList.append(room)
      s = room.modifiers.new(type='SOLIDIFY', name='S')
      s.thickness = -0.3
      bpy.ops.object.modifier_apply(modifier='S')
      room.select = False
      bpy.context.scene.objects.active = None

      print("Generating door hole.")
      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0),layers=self.firstLayer)
      door = bpy.data.objects['Cube']
      door.select = True
      bpy.context.scene.objects.active = door
      door.dimensions = ((6.5 * 0.55), 1, self.officeSize[2] * 0.75)
      door.location = ((self.currentBounds[2][0] + self.currentBounds[3][0]) / 2, (self.currentBounds[2][1] - 0.3), (self.officeSize[2] * 0.75) / 2)

      door.select = False
      room.select = True
      bpy.context.scene.objects.active = room
      b1 = room.modifiers.new(type='BOOLEAN', name='B1')
      b1.operation = 'DIFFERENCE'
      b1.object = door
      bpy.ops.object.modifier_apply(modifier='B1')
      room.select = False
      door.select = True
      bpy.ops.object.delete()
      bpy.context.scene.update()
      door.select = False
      bpy.context.scene.objects.active = None

      print("Generating window hole.")
      bpy.ops.mesh.primitive_cube_add(radius=10, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=self.firstLayer)
      window = bpy.data.objects['Cube']
      window.select = True
      bpy.context.scene.objects.active = window
      window.dimensions = ((self.currentBounds[1][0] - self.currentBounds[0][0]) * 0.6, 1, self.officeSize[2] * 0.3)
      window.location = ((self.currentBounds[0][0] + self.currentBounds[1][0]) / 2, self.currentBounds[1][1] - 0.3, (self.officeSize[2]) / 1.5)

      window.select = False
      room.select = True
      bpy.context.scene.objects.active = room
      b2 = room.modifiers.new(type='BOOLEAN', name='B2')
      b2.operation = 'DIFFERENCE'
      b2.object = window
      bpy.ops.object.modifier_apply(modifier='B2')
      room.select = False
      window.select = True
      bpy.ops.object.delete()
      bpy.context.scene.update()
      window.select = False
      bpy.context.scene.objects.active = None

      print("Turning on the lights.")
      degrees = random.uniform(0,0.5)*2-0.5
      scene = bpy.context.scene
      lampName = "Lamp1_" + str(self.roomsCounter)
      lamp_data1 = bpy.data.lamps.new(name=lampName, type='HEMI')
      lamp_data1.energy = 0.25
      lamp_object1 = bpy.data.objects.new(name=lampName, object_data=lamp_data1)

      scene.objects.link(lamp_object1)

      lamp_object1.location = (room.location[0], room.location[1], (self.officeSize[2] - (5 * 0.35)))
      lamp_object1.select = True
      bpy.ops.transform.rotate(value=degrees, axis=(0, 1, 0), constraint_orientation='GLOBAL')
      lamp_object1.select = False

      lampName = "Lamp2_" + str(self.roomsCounter)
      lamp_data2 = bpy.data.lamps.new(name=lampName, type='HEMI')
      lamp_data2.energy = 0.25
      lamp_object2 = bpy.data.objects.new(name=lampName, object_data=lamp_data2)

      scene.objects.link(lamp_object2)

      lamp_object2.location = (room.location[0], room.location[1] + (self.officeSize[1] / 3), (self.officeSize[2] - (5 * 0.35)))
      lamp_object2.select = True
      bpy.ops.transform.rotate(value=degrees, axis=(0, 1, 0), constraint_orientation='GLOBAL')
      lamp_object2.select = False

      lampName = "Lamp3_" + str(self.roomsCounter)
      lamp_data3 = bpy.data.lamps.new(name=lampName, type='HEMI')
      lamp_data3.energy = 0.25
      lamp_object3 = bpy.data.objects.new(name=lampName, object_data=lamp_data3)

      scene.objects.link(lamp_object3)

      lamp_object3.location = (room.location[0], room.location[1] - (self.officeSize[0] / 3), (self.officeSize[2] - (5 * 0.35)))
      lamp_object3.select = True
      bpy.ops.transform.rotate(value=degrees, axis=(0, 1, 0), constraint_orientation='GLOBAL')
      lamp_object3.select = False
      bpy.ops.object.select_all(action='DESELECT')

      print("\n---- ROOM %d SUCCESSFULLY GENERATED! ----\n" % self.roomsCounter)

      if self.upsideDown:
         for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
               for region in area.regions:
                  if region.type == 'WINDOW':
                     override = {'area': area, 'region': region}
         bpy.context.scene.objects.active = room
         room.rotation_mode = 'AXIS_ANGLE'
         for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
               area.spaces.active.pivot_point='CURSOR'
               area.spaces.active.cursor_location = (room.location[0], room.location[1], 0)
         for l in self.generatedList:
            l.select = True
            l.rotation_mode = 'AXIS_ANGLE'
         room.select = True
         bpy.ops.transform.rotate(override, value=math.radians(180), axis=(0, 0, 1), constraint_orientation='LOCAL')
         for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
               area.spaces.active.pivot_point='MEDIAN_POINT'
         bpy.context.scene.objects.active = None
         bpy.ops.object.select_all(action='DESELECT')
      self.generatedList.clear()






   def nothing(self):
      pass

   def generateGeometry(self, environmentString):
      print("\n--- STARTING OFFICE FLOOR GENERATION ---\n")
      b,m=0,0
      if self.bathroomSize[0] != 0:
         b=1
      if self.meetingSize[0] != 0:
         m=1
      grammars = [str(x.strip()) for x in environmentString.split('F')]
      for g in range(len(grammars)-1):
         grammars[g] += "F"
      print(grammars)
      task = -1
      availableTasks = [0, 1*m, 2*b]
      side = 0 #side to work with (0->up, 1->down)
      for r in range(self.roomNumberUpOriginal + self.roomNumberDownOriginal + b + m):
         if len(self.noises) == 1:
            self.currentNoise = self.noises[0]
         else:
            self.currentNoise = self.noises.pop(0)
         # let's decide randomly what's next (0->office room, 1->meeting, 2->bathroom)
         # if last task was 0 ad there are rooms left, next task will be 0 again
         # completedTasks 1 and 2 cannot be done twice in the same side AND environment
         if side == 0:
            if task == 0 and self.roomNumberUpLeft > 0:
               self.completedTasks.append(0)
               self.roomNumberUpLeft -= 1
            elif len(self.completedTasks) == max(self.roomNumberUpOriginal + b, self.roomNumberUpOriginal + m):
               self.lastSurface = []
               self.upsideDown = True
               side = 1
            else:
               while True:
                  r = random.choice(availableTasks)
                  if r not in self.completedTasks:
                     if (r == 1 and 2 not in self.completedTasks) or (r == 2 and 1 not in self.completedTasks):
                        task = r
                        self.completedTasks.append(task)
                        break
                     elif r == 0 and self.roomNumberUpLeft > 0:
                        task = r
                        self.completedTasks.append(task)
                        self.roomNumberUpLeft -= 1
                        break
         if side == 1:
            if task == 0 and self.roomNumberDownLeft > 0:
               self.completedTasks.append(0)
               self.roomNumberDownLeft -= 1
            elif len(self.completedTasks) == self.roomNumberUpOriginal + self.roomNumberDownOriginal + b + m:
               side = -1
            else:
               while True:
                  r = random.choice(availableTasks)
                  if (r not in self.completedTasks):
                     task = r
                     self.completedTasks.append(task)
                     break
                  elif (r == 0 and self.roomNumberDownLeft > 0):
                     task = r
                     self.completedTasks.append(task)
                     self.roomNumberDownLeft -= 1
                     break
         if side >= 0:
            print("Side: ", side)
            print("Available tasks: ",availableTasks)
            print("Chosen: ",task)
            print("Completed: ",self.completedTasks)
            print("Grammar: ",grammars[task])
            self.initializeNextSurface(task, side)


            for i in grammars[task]:
               if(i in self.commands):
                  self.commands[i](self)
               else:
                  self.commands[i]=ProceduralGeometry.nothing
            #self.recoverContext()
            self.roomsCounter += 1

      self.upsideDown = False
      self.generateCorridor(m, b)

   commands['R'] = generateFloorAndWalls
   commands['M'] = generateMeetingBounds
   commands['W'] = generateWorkBounds
   commands['V'] = generateShelving
   commands['K'] = generateMeetingDesk
   commands['J'] = generateLargeMeetingDesk
   commands['T'] = generateDeskType1
   commands['Y'] = generateDeskType2
   commands['H'] = generateChairType1
   commands['A'] = generateChairType2
   commands['B'] = generateBin
   commands['P'] = generateCorkPanel
   commands['Q'] = generateProjectorPanel
   commands['L'] = generateReadingLamp
   commands['N'] = generateMonitor
   commands['O'] = generateKeyboardAndMouse
   commands['G'] = generateClothHanger
   commands['I'] = generateBathroom
   commands['['] = saveContext
   commands[']'] = recoverContext
   commands['F'] = finishRoom

