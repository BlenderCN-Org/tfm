#############################################################################
#                Materials and textures generator code                      #
#############################################################################

import bmesh, bpy, random, sys, copy

class Materials(object):

    def __init__(self):
        self.pymat = bpy.data.materials

    def woodMaterial(self,mat):
      mat.diffuse_shader = 'LAMBERT'
      mat.diffuse_intensity = 1.0
      mat.specular_color = (1.0, 1.0, 1.0)
      mat.specular_shader = 'COOKTORR'
      mat.specular_intensity = random.uniform(0.05, 0.2)
      mat.alpha = 1
      mat.ambient = 1

    def grayMaterial(self,mat):
      mat.diffuse_shader = 'LAMBERT'
      mat.diffuse_intensity = random.uniform(0.3, 0.85)
      mat.specular_color = (0.7, 0.7, 0.7)
      mat.specular_shader = 'COOKTORR'
      mat.specular_intensity = random.uniform(0.05, 0.2)
      mat.alpha = 1
      mat.ambient = 1

    def colorMaterial(self,mat):
      mat.diffuse_shader = 'LAMBERT'
      mat.diffuse_intensity = random.uniform(0.1, 0.7)
      mat.specular_color = (1.0, 1.0, 1.0)
      mat.specular_shader = 'COOKTORR'
      mat.specular_intensity = 0.0
      mat.alpha = 1
      mat.ambient = 1

    def woodTexture(self,mat,mat_diffuse):
        # creates first basis texture---------------------------------------------------
        #-common parameters-
        name1 = "Basis"
        tex = bpy.data.textures.new(name1, 'WOOD')
        slot = mat.texture_slots.add()
        slot.mapping = 'FLAT'
        slot.texture_coords = 'GLOBAL'
        slot.use_rgb_to_intensity = True
        adding = random.uniform(0.1, 0.22)
        scale = random.uniform(0.1, 0.5)

        #-wood type and color-
        r = 0
        noisebasis2 = ['SIN', 'SAW', 'TRI']
        woodtype = ['BANDS', 'RINGS', 'BANDNOISE', 'RINGNOISE']
        noisetype = ['SOFT_NOISE', 'HARD_NOISE']
        noisebasis = ['BLENDER_ORIGINAL', 'ORIGINAL_PERLIN', 'IMPROVED_PERLIN', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2_F1', 'VORONOI_CRACKLE', 'CELL_NOISE']

        r = random.randint(0, len(noisebasis2) - 1)
        tex.noise_basis_2 = noisebasis2[r]
        r = random.randint(0, len(woodtype) - 1)
        tex.wood_type = woodtype[r]
        if (tex.wood_type == 'BANDS' or tex.wood_type == 'RINGS') and (tex.noise_basis_2 == 'SIN' or tex.noise_basis_2 == 'TRI'):
            mat_diffuse[0] = min(1.0, mat_diffuse[0] - adding + 0.07)
        else:
            mat_diffuse[0] = min(1.0, mat_diffuse[0] - adding)
        mat_diffuse[1] = mat_diffuse[0] * 0.52
        mat_diffuse[2] = mat_diffuse[0] * 0.31
        slot.color = tuple(mat_diffuse)
        r = random.randint(0, len(noisetype) - 1)
        tex.noise_type = noisetype[r]
        r = random.randint(0, len(noisebasis) - 1)
        tex.noise_basis = noisebasis[r]
        r = random.uniform(0.15, 1.5)
        tex.noise_scale = r
        slot.diffuse_color_factor = random.uniform(0.4, 0.7)
        slot.scale = (scale, 1.0, 1.0)

        #-apply it-
        slot.texture = tex

        # creates basis complementing texture---------------------------------------------------
        #-common parameters-
        name2 = "Comp"
        tex2 = bpy.data.textures.new(name2, 'WOOD')
        slot2 = mat.texture_slots.add()
        slot2.mapping = 'FLAT'
        slot2.texture_coords = 'GLOBAL'
        slot2.use_rgb_to_intensity = True
        adding = random.uniform(0.1, 0.2)

        #-wood type and color according to basis-
        if tex.wood_type == 'BANDS':
            tex2.wood_type = 'BANDNOISE'
        elif tex.wood_type == 'RINGS':
            tex2.wood_type = 'RINGNOISE'
        elif tex.wood_type == 'BANDNOISE':
            tex2.wood_type = 'BANDS'
        else:
            tex2.wood_type = 'RINGS'
        mat_diffuse[0] = min(1.0, mat_diffuse[0] - adding)
        mat_diffuse[1] = mat_diffuse[0] * 0.52
        mat_diffuse[2] = mat_diffuse[0] * 0.31
        slot2.color = tuple(mat_diffuse)
        #slot2.blend_type = 'ADD'

        slot2.diffuse_color_factor = random.uniform(0.7, 1)
        tex2.noise_basis_2 = tex.noise_basis_2
        tex2.noise_basis = tex.noise_basis
        tex2.noise_type = tex.noise_type
        tex2.noise_scale = tex.noise_scale
        slot2.diffuse_color_factor = 1 - slot.diffuse_color_factor - random.uniform(0.1, 0.25)
        slot2.scale = (scale, 1.0, 1.0)

        #-apply it-
        slot2.texture = tex2

        # creates noise texture---------------------------------------------------
        #-common parameters-
        name3 = "Noise"
        tex3 = bpy.data.textures.new(name3, 'CLOUDS')
        slot3 = mat.texture_slots.add()
        slot3.mapping = 'FLAT'
        slot3.texture_coords = 'GLOBAL'
        slot3.use_rgb_to_intensity = True
        adding = random.uniform(0.05, 0.1)

        #-clouds type and color according to basis
        size = random.uniform(0.5, 1)
        tex3.noise_scale = size
        del noisebasis[-1]
        r = random.randint(0, len(noisebasis) - 1)
        tex3.noise_basis = noisebasis[r]
        r = random.randint(0, len(noisetype) - 1)
        tex3.noise_type = 'SOFT_NOISE'
        mat_diffuse[0] = min(1.0, mat_diffuse[0] - adding)
        mat_diffuse[1] = mat_diffuse[0] * 0.52
        mat_diffuse[2] = mat_diffuse[0] * 0.31
        slot3.color = tuple(mat_diffuse)
        slot3.diffuse_color_factor = 1 - slot.diffuse_color_factor - slot2.diffuse_color_factor

        #-apply it-
        slot3.texture = tex3


    def createWood(self,mat):
        print("Generating wood material.")
        # ------ material section ------
        try:
            bpy.data.materials.remove(bpy.data.materials['Wood2'])
            bpy.data.materials.remove(bpy.data.materials['Wood3'])
            mat2 = bpy.data.materials.new('Wood2')
            mat3 = bpy.data.materials.new('Wood3')
        except:
            mat2 = bpy.data.materials.new('Wood2')
            mat3 = bpy.data.materials.new('Wood3')
        self.woodMaterial(mat)
        (r, g, b) = mat.diffuse_color
        mat2.diffuse_color = (min((r+r*0.4),1), min((g+g*0.4),1), min((b+b*0.4),1))
        mat3.diffuse_color = (max((r-r*0.4),0), max((g-g*0.4),0), max((b-b*0.4),0))
        self.woodMaterial(mat2)
        self.woodMaterial(mat3)
        # ------ texture section ------
        for s in range(len(mat.texture_slots)):
            mat.texture_slots.clear(s)
        (r, g, b) = mat.diffuse_color
        diffuse = [r, g, b]
        self.woodTexture(mat, diffuse)
        for s in range(len(mat2.texture_slots)):
            mat2.texture_slots.clear(s)
        (r, g, b) = mat2.diffuse_color
        diffuse = [r, g, b]
        self.woodTexture(mat2, diffuse)
        for s in range(len(mat3.texture_slots)):
            mat3.texture_slots.clear(s)
        (r, g, b) = mat3.diffuse_color
        diffuse = [r, g, b]
        self.woodTexture(mat3, diffuse)


    def createGrayscale(self,mat):
        print("Generating grayscale material.")
        # ------ material section ------
        self.grayMaterial(mat)


    def createColor(self,mat):
        print("Generating color material.")
        # ------ material section ------
        self.colorMaterial(mat)

    def createWallMaterial(self):
        print("Creating walls material.")
        mat = bpy.data.materials.new('Walls')
        r = min(1.0, random.uniform(-0.05, 0.05) + 0.84)
        g = random.uniform(-0.1, 0.1) + 0.76
        b = random.uniform(-0.25, 0.25) + 0.33
        mat.diffuse_color = (r, g, b)
        mat.diffuse_shader = 'LAMBERT'
        mat.diffuse_intensity = 1.0
        mat.specular_color = (1.0, 1.0, 1.0)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.0
        mat.ambient = 1

    def createFloorMaterial(self):
        print("Creating floor material.")
        mat = bpy.data.materials.new('Floor')
        mat.diffuse_color = (0.1, 0.1, 0.1)
        mat.diffuse_shader = 'LAMBERT'
        mat.diffuse_intensity = random.uniform(0.6, 1.0)
        mat.specular_color = (mat.diffuse_color[0] + 0.1, mat.diffuse_color[1] + 0.1, mat.diffuse_color[2] + 0.1)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.3
        mat.ambient = 1

    def generateNewMaterials(self):
        print("")
        for m in self.pymat:
            if m.name == "Wood":
                self.createWood(m)
            if m.name == "Grayscale":
                self.createGrayscale(m)
            if m.name == "Color":
                self.createColor(m)
        try:
            bpy.data.materials.remove(bpy.data.materials['Walls'])
            bpy.data.materials.remove(bpy.data.materials['Floor'])
            self.createWallMaterial()
            self.createFloorMaterial()
        except:
            self.createWallMaterial()
            self.createFloorMaterial()


