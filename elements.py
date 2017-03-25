#############################################################################
#             Room elements modification and allocation code                #
#############################################################################

import random
import bpy
import bmesh
import math

class Elements(object):


    def move(self,eje,cant):
        if eje == "x":
            bpy.ops.transform.translate(value=(cant, 0, 0), constraint_orientation='LOCAL',)
        if eje == "y":
            bpy.ops.transform.translate(value=(0, cant, 0), constraint_orientation='LOCAL')
        if eje == "z":
            bpy.ops.transform.translate(value=(0, 0, cant), constraint_orientation='LOCAL')

    def scale(self,eje,cant):
        if eje == "x":
            bpy.ops.transform.resize(value=(cant, cant, cant), constraint_axis=(True, False, False), constraint_orientation='LOCAL',)
        if eje == "y":
            bpy.ops.transform.resize(value=(cant, cant, cant), constraint_axis=(False, True, False), constraint_orientation='LOCAL')
        if eje == "z":
            bpy.ops.transform.resize(value=(cant, cant, cant), constraint_axis=(False, False, True), constraint_orientation='LOCAL')

    def rotate(self,eje,cant):
        if eje == "x":
            bpy.ops.transform.rotate(value=cant, axis=(1, 0, 0), constraint_orientation='GLOBAL',)
        if eje == "y":
            bpy.ops.transform.rotate(value=cant, axis=(0, 1, 0), constraint_orientation='GLOBAL')
        if eje == "z":
            bpy.ops.transform.rotate(value=cant, axis=(0, 0, 1), constraint_orientation='GLOBAL')

    def duplicate(self, meshName):
        meshes = [object for object in bpy.context.scene.objects if object.name == meshName]
        requestedMesh = meshes[0]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[0] = True
        bpy.context.scene.layers[1] = True
        requestedMesh.select = True
        bpy.context.scene.objects.active = requestedMesh
        bpy.ops.object.duplicate()
        duplicatedName = meshName + ".0"
        duplicatedMesh = [object for object in bpy.context.scene.objects if duplicatedName in object.name]
        requestedMesh.select = False
        duplicatedMesh[0].select = True
        bpy.context.scene.objects.active = duplicatedMesh[0]
        return duplicatedMesh[0]

    def putShelving(self, bounds, orientation):
        duplicatedMesh = self.duplicate("Shelving")
        mat = random.randint(6,8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        r = random.gauss(1, 0.1)
        self.scale('y', r)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')
        if orientation == 'L':
            x = bounds[0][0] + (2 * 0.35)
            y = random.uniform(bounds[0][1] - (5.2 * 0.35), bounds[2][1] + (5 * 0.35))
            duplicatedMesh.location = (x, y, 0)
            duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
            duplicatedMesh.rotation_axis_angle = (math.radians(0), 0, 0, 1)
        else:
            x = bounds[1][0] - (2 * 0.35)
            y = random.uniform(bounds[1][1] - (5.2 * 0.35), bounds[3][1] + (5 * 0.35))
            duplicatedMesh.location = (x, y, 0)
            duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
            duplicatedMesh.rotation_axis_angle = (math.radians(180), 0, 0, 1)
        print("Generating shelving on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return duplicatedMesh

    def putMeetingDesk(self, bounds):
        duplicatedMesh = self.duplicate("Desk1")

        mat = random.randint(6,8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)

        length = [0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33,
                 46, 70, 71, 75, 76, 77, 79, 80, 82, 84]
        width = [0, 1, 3, 4, 5, 6, 7, 8, 9, 22, 28, 29, 30, 32, 33, 34, 35, 37, 38, 45, 46, 47, 48, 50, 51, 65, 67, 68,
                 69, 71, 73, 74, 75, 80, 81, 82, 85]
        height = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 29,
                30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
                56, 57, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69]

        # length-------------------
        l = random.gauss(0, 0.8)
        #bm.faces.ensure_lookup_table()
        for i in length:
            bm.faces[i].select = True
        self.move("y", l)
        bpy.ops.mesh.select_all(action='DESELECT')

        # width-------------------
        w = random.gauss(0, 0.8)
        #bm.faces.ensure_lookup_table()
        for i in width:
            bm.faces[i].select = True
        self.move("x", w)
        bpy.ops.mesh.select_all(action='DESELECT')

        # height-------------------
        h = random.gauss(0, 0.6)
        #bm.faces.ensure_lookup_table()
        for i in height:
            bm.faces[i].select = True
        self.move("z", h)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
        True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
        False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')
        #x = random.uniform(bounds[0][0] + 13, bounds[1][0] - 10)
        x = random.uniform(bounds[0][0] + (13 * 0.35), bounds[1][0] - (13 * 0.35))
        y = random.uniform(((bounds[0][1] + bounds[2][1]) / 2) - 0, ((bounds[0][1] + bounds[2][1]) / 2) + (2 * 0.35))
        duplicatedMesh.location = (x, y, 0)
        xd = duplicatedMesh.dimensions[0]
        yd = duplicatedMesh.dimensions[1]
        zd = duplicatedMesh.dimensions[2]
        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        duplicatedMesh.rotation_axis_angle = (math.radians(-90), 0, 0, 1)
        print("Generating meeting desk on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return [2, x, y, xd, 90, yd, zd, duplicatedMesh]

    def putLargeMeetingDesk(self, bounds):
        duplicatedMesh = self.duplicate("Desk4")

        mat = random.randint(6, 8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)

        length = [0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33,
                  46, 70, 71, 75, 76, 77, 79, 80, 82, 84]
        width = [0, 1, 3, 4, 5, 6, 7, 8, 9, 22, 28, 29, 30, 32, 33, 34, 35, 37, 38, 45, 46, 47, 48, 50, 51, 65, 67, 68,
                 69, 71, 73, 74, 75, 80, 81, 82, 85]
        height = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 29,
                  30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
                  55,
                  56, 57, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69]

        # length-------------------
        l = random.gauss(0, 0.8)
        # bm.faces.ensure_lookup_table()
        for i in length:
            bm.faces[i].select = True
        self.move("y", l)
        bpy.ops.mesh.select_all(action='DESELECT')

        # width-------------------
        w = random.gauss(0, 0.8)
        # bm.faces.ensure_lookup_table()
        for i in width:
            bm.faces[i].select = True
        self.move("x", w)
        bpy.ops.mesh.select_all(action='DESELECT')

        # height-------------------
        h = random.gauss(0, 0.6)
        # bm.faces.ensure_lookup_table()
        for i in height:
            bm.faces[i].select = True
        self.move("z", h)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')
        # x = random.uniform(bounds[0][0] + 13, bounds[1][0] - 10)
        x = (bounds[0][0] + bounds[1][0]) / 2
        y = (bounds[0][1] + bounds[2][1]) / 2
        duplicatedMesh.location = (x, y, 0)
        xd = duplicatedMesh.dimensions[0]
        yd = duplicatedMesh.dimensions[1]
        zd = duplicatedMesh.dimensions[2]
        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        duplicatedMesh.rotation_axis_angle = (math.radians(90), 0, 0, 1)
        print("Generating meeting desk on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return [4, x, y, xd, 90, yd, zd, duplicatedMesh]

    def putDeskType1(self, bounds):
        duplicatedMesh = self.duplicate("Desk2")

        mat = random.randint(6,8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)

        length = [4, 5, 6, 7, 8, 9, 15, 16, 23, 25, 27, 28, 29, 30, 32, 35, 38, 40, 41, 42, 49, 50, 51, 53, 57, 59, 60,
                 62, 66, 67, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
                 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
                 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133,
                 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153,
                 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173,
                 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187]
        width = [2, 7, 11, 14, 16, 21, 26, 27, 28, 35, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 65]

        # length-------------------
        l = random.gauss(0, 0.4)
        #bm.faces.ensure_lookup_table()
        for i in length:
            bm.faces[i].select = True
        self.move("y", l)
        bpy.ops.mesh.select_all(action='DESELECT')

        # width-------------------
        w = random.gauss(0, 0.4)
        #bm.faces.ensure_lookup_table()
        for i in width:
            bm.faces[i].select = True
        self.move("x", w)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')
        x = random.uniform(bounds[0][0] + (10 * 0.35), bounds[1][0] - (10 * 0.35))
        y = (bounds[0][1] + bounds[2][1]) / 2 - random.uniform(0,1)
        duplicatedMesh.location = (x, y, 0)
        xd = duplicatedMesh.dimensions[0]
        yd = duplicatedMesh.dimensions[1]
        zd = duplicatedMesh.dimensions[2]
        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        if random.uniform(0, 1) > 0.5:
            o = 90
            duplicatedMesh.rotation_axis_angle = (math.radians(90), 0, 0, 1)
        else:
            o = 270
            duplicatedMesh.rotation_axis_angle = (math.radians(270), 0, 0, 1)
        print("Generating type 1 desk on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return [1, x, y, xd, o, yd, zd, duplicatedMesh]

    def putDeskType2(self, bounds):
        duplicatedMesh = self.duplicate("Desk3")

        mat = random.randint(6,8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)

        length = [4, 5, 6, 7, 8, 9, 14, 17, 20, 28, 31, 34, 35, 36, 43, 44, 45, 48, 51, 54, 57, 58, 64, 67, 68, 69, 71,
                 78, 79, 80, 81, 84, 85, 87, 89, 90, 92, 94, 95, 98, 99, 102, 103, 104, 107, 109, 110, 111, 113, 114,
                 117, 119, 120, 123, 124, 125, 129, 132, 137, 139, 140, 142, 144, 145, 147, 148, 150, 151, 152, 155,
                 156, 158, 159, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178,
                 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198,
                 199, 200, 201, 202, 203]
        width = [2, 7, 11, 20, 21, 22, 32, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 58]

        # length-------------------
        l = random.gauss(0, 0.4)
        #bm.faces.ensure_lookup_table()
        for i in length:
            bm.faces[i].select = True
        self.move("y", l)
        bpy.ops.mesh.select_all(action='DESELECT')

        # width-------------------
        w = random.gauss(0, 0.4)
        #bm.faces.ensure_lookup_table()
        for i in width:
            bm.faces[i].select = True
        self.move("x", w)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        x = random.uniform(bounds[0][0] + (10 * 0.35), bounds[1][0] - (10 * 0.35))
        y = (bounds[0][1] + bounds[2][1]) / 2 - random.uniform(0, 1)
        duplicatedMesh.location = (x, y, 0)
        xd = duplicatedMesh.dimensions[0]
        yd = duplicatedMesh.dimensions[1]
        zd = duplicatedMesh.dimensions[2]
        if random.uniform(0, 1) > 0.5:
            o = 90
            duplicatedMesh.rotation_axis_angle = (math.radians(90), 0, 0, 1)
        else:
            o = 270
            duplicatedMesh.rotation_axis_angle = (math.radians(270), 0, 0, 1)
        print("Generating type 2 desk on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return [1, x, y, xd, o, yd, zd, duplicatedMesh]

    def putChairType1(self, deskData, noise):
        chairs = 0
        chairList = []
        for i in range(deskData[0]):
            duplicatedMesh = self.duplicate("Chair1")

            seat = [172, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
                       211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230,
                       231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250,
                       251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270,
                       271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290,
                       291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310,
                       311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330,
                       331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350,
                       351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370,
                       371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390,
                       391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
                       411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430,
                       431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450,
                       451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470,
                       471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490,
                       491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510,
                       511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530,
                       531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550,
                       551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567]
            back = [402, 406, 407, 408, 409, 410, 411, 413, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493,
                        494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513,
                        514, 515, 516, 517, 518, 519, 520, 521, 522, 523]

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bm = bmesh.from_edit_mesh(bpy.context.object.data)

            # seat height -------------------
            r = random.gauss(0.2, 0.5)
            #bm.faces.ensure_lookup_table()
            for i in seat:
                bm.faces[i].select = True
            self.move("z", r)
            bpy.ops.mesh.select_all(action='DESELECT')

            # back height-------------------
            r = random.gauss(0.5, 0.6)
            #bm.faces.ensure_lookup_table()
            for i in back:
                bm.faces[i].select = True
            self.move("z", r)
            bpy.ops.mesh.select_all(action='DESELECT')

            bpy.ops.object.mode_set(mode='OBJECT')
            self.scale('x', 0.35)
            self.scale('y', 0.35)
            self.scale('z', 0.35)
            bpy.ops.object.move_to_layer(layers=(
                True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False,
                False, False, False, False))
            bpy.ops.object.select_all(action='DESELECT')

            if chairs == 0:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                if deskData[4] == 90:
                    x = deskData[1] - (random.randint(0, 1)*2-1) * noise * random.uniform(0,deskData[3]/3) * (deskData[0]-1)
                    y = deskData[2] - deskData[3]/2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(deskData[4] + 180 + (random.randint(0, 1)*2-1) * noise * random.uniform(10,20) * (deskData[0]-1)), 0, 0, 1)
                else:
                    x = deskData[1] - (random.randint(0, 1)*2-1) * noise * random.uniform(0,deskData[3]/3) * (deskData[0]-1)
                    y = deskData[2] + deskData[3]/2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(deskData[4] + 180 + (random.randint(0, 1)*2-1) * noise * random.uniform(10,20) * (deskData[0]-1)), 0, 0, 1)
            if chairs == 1:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                if deskData[4] == 90:
                    x = deskData[1] - (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[3] / 3) * (
                    deskData[0] - 1)
                    y = deskData[2] + deskData[3] / 2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(
                        deskData[4] + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (
                        deskData[0] - 1)), 0, 0, 1)
                else:
                    x = deskData[1] - (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[3] / 3) * (
                    deskData[0] - 1)
                    y = deskData[2] - deskData[3] / 2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(
                        deskData[4] + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (
                        deskData[0] - 1)), 0, 0, 1)
            if chairs == 2:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                x = deskData[1] + deskData[5] / 2
                y = deskData[2] - (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[5] / 3) * (deskData[0] - 1)
                duplicatedMesh.location = (x, y, 0)
                duplicatedMesh.rotation_axis_angle = (math.radians(
                    deskData[4] - 90 + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (deskData[0] - 1)), 0, 0, 1)
            if chairs == 3:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                x = deskData[1] - deskData[5] / 2
                y = deskData[2] + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[5] / 3) * (deskData[0] - 1)
                duplicatedMesh.location = (x, y, 0)
                duplicatedMesh.rotation_axis_angle = (math.radians(
                    deskData[4] + 90 + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (deskData[0] - 1)), 0, 0, 1)
            print("Generating type 1 chair on ", tuple(duplicatedMesh.location))
            chairs += 1
            duplicatedMesh.select = False
            bpy.context.scene.objects.active = None
            bpy.context.scene.layers[1] = False
            bpy.context.scene.layers[0] = True

            chairList.append(duplicatedMesh)
        return chairList

    def putChairType2(self, deskData, noise):
        chairs = 0
        chairList = []
        for i in range(deskData[0]):
            duplicatedMesh = self.duplicate("Chair2")
            mat = random.randint(6,8)
            duplicatedMesh.data.materials[1] = bpy.data.materials[mat]
            width = [0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 28, 29, 30, 31, 32, 33, 34,
                     35, 36, 37, 38, 40, 41, 42, 43, 47, 49, 51, 52, 54, 55, 56, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68,
                     69, 70, 71, 72, 78, 79, 80, 81, 82, 83, 85, 87, 88, 90, 91, 92, 94, 95, 97, 98, 99, 100, 101, 102,
                     103, 104, 105, 106, 107, 108, 114, 115, 116, 117, 118]
            chairHeight = [1, 2, 3, 4, 6, 10, 11, 12, 14, 15, 16, 17, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                         35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                         59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,
                         83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104,
                         105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 121, 122, 123, 125,
                         129, 130, 131, 133, 134, 135, 136, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152,
                         153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                         172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
                         191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209,
                         210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228,
                         229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247,
                         248, 249, 250, 251, 252]
            backHeight = [11, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 44, 45, 46, 83, 84, 85, 86, 87, 88, 89,
                            90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                            110, 111, 112, 113, 114, 115, 116, 117, 118, 130, 149, 150, 151, 152, 153, 154, 155, 156,
                            157, 158, 159, 160, 165, 166, 167, 168, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
                            221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238,
                            239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252]

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bm = bmesh.from_edit_mesh(bpy.context.object.data)

            # width-------------------
            r = random.gauss(0, 0.1)
            #bm.faces.ensure_lookup_table()
            for i in width:
                bm.faces[i].select = True
            self.move("x", r)
            bpy.ops.mesh.select_all(action='DESELECT')

            # chairHeight-------------------
            r = random.gauss(0, 0.2)
            #bm.faces.ensure_lookup_table()
            for i in chairHeight:
                bm.faces[i].select = True
            self.move("z", r)
            bpy.ops.mesh.select_all(action='DESELECT')

            # backHeight-------------------
            r = random.gauss(0, 0.4)
            #bm.faces.ensure_lookup_table()
            for i in backHeight:
                bm.faces[i].select = True
            self.move("z", r)
            bpy.ops.mesh.select_all(action='DESELECT')

            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.smart_project()
            bpy.ops.mesh.select_all(action='DESELECT')

            bpy.ops.object.mode_set(mode='OBJECT')
            self.scale('x', 0.35)
            self.scale('y', 0.35)
            self.scale('z', 0.35)
            bpy.ops.object.move_to_layer(layers=(
                True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                False,
                False, False, False, False))
            bpy.ops.object.select_all(action='DESELECT')
            if chairs == 0:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                if deskData[4] == 90:
                    x = deskData[1] - (random.randint(0, 1)*2-1) * noise * random.uniform(0,deskData[3]/3) * (deskData[0]-1)
                    y = deskData[2] - deskData[3]/2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(deskData[4] + 180 + (random.randint(0, 1)*2-1) * noise * random.uniform(10,20) * (deskData[0]-1)), 0, 0, 1)
                else:
                    x = deskData[1] - (random.randint(0, 1)*2-1) * noise * random.uniform(0,deskData[3]/3) * (deskData[0]-1)
                    y = deskData[2] + deskData[3]/2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(deskData[4] + 180 + (random.randint(0, 1)*2-1) * noise * random.uniform(10,20) * (deskData[0]-1)), 0, 0, 1)
            if chairs == 1:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                if deskData[4] == 90:
                    x = deskData[1] - (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[3] / 3) * (
                    deskData[0] - 1)
                    y = deskData[2] + deskData[3] / 2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(
                        deskData[4] + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (
                        deskData[0] - 1)), 0, 0, 1)
                else:
                    x = deskData[1] - (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[3] / 3) * (
                    deskData[0] - 1)
                    y = deskData[2] - deskData[3] / 2
                    duplicatedMesh.location = (x, y, 0)
                    duplicatedMesh.rotation_axis_angle = (math.radians(
                        deskData[4] + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (
                        deskData[0] - 1)), 0, 0, 1)
            if chairs == 2:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                x = deskData[1] + deskData[5] / 2
                y = deskData[2] - (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[5] / 3) * (deskData[0] - 1)
                duplicatedMesh.location = (x, y, 0)
                duplicatedMesh.rotation_axis_angle = (math.radians(
                    deskData[4] - 90 + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (deskData[0] - 1)), 0, 0, 1)
            if chairs == 3:
                duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
                x = deskData[1] - deskData[5] / 2
                y = deskData[2] + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(0, deskData[5] / 3) * (deskData[0] - 1)
                duplicatedMesh.location = (x, y, 0)
                duplicatedMesh.rotation_axis_angle = (math.radians(
                    deskData[4] + 90 + (random.randint(0, 1) * 2 - 1) * noise * random.uniform(10, 20) * (deskData[0] - 1)), 0, 0, 1)
            print("Generating type 1 chair on ", tuple(duplicatedMesh.location))
            chairs += 1
            duplicatedMesh.select = False
            bpy.context.scene.objects.active = None
            bpy.context.scene.layers[1] = False
            bpy.context.scene.layers[0] = True
            chairList.append(duplicatedMesh)
        return chairList

    def putBin(self, corner1, corner2, orientation):
        duplicatedMesh = self.duplicate("Bin")

        border = [30, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
                 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
                 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127,
                 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147,
                 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160]

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)

        # height-------------------
        r = random.gauss(0, 0.3)
        #bm.faces.ensure_lookup_table()
        for i in border:
            bm.faces[i].select = True
        self.move("z", r)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        y = random.uniform(corner1[1] - (5 * 0.35), corner2[1] + (2.5 * 0.35))
        if orientation == 'R':
            x = corner1[0] - (2.5 * 0.35)
        else:
            x = corner1[0] + (2.5 * 0.35)
        duplicatedMesh.location = (x, y, 0)
        print("Generating bin on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return duplicatedMesh

    def putCorkPanel(self, corner1, corner2, wallHeight, noise, orientation):
        duplicatedMesh = self.duplicate("CorkPanel")

        mat = random.randint(6,8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        r = random.gauss(1, 0.05)
        self.scale('x', r)
        r = random.gauss(1, 0.03)
        self.scale('z', r)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
        True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
        False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')
        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'

        y = (corner1[1] + corner2[1]) / 2 + random.uniform(-1,1)
        if orientation == 'R':
            x = corner1[0] - (0.5 * 0.35)
            duplicatedMesh.rotation_axis_angle = (math.radians(180), 0, 0, 1)
        else:
            x = corner1[0] + (0.5 * 0.35)
            duplicatedMesh.rotation_axis_angle = (math.radians(0), 0, 0, 1)
        duplicatedMesh.location = (x, y, wallHeight / 2)
        print("Generating cork panel on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return duplicatedMesh

    def putProjectorPanel(self, corner1, corner2, wallHeight, orientation):
        duplicatedMesh = self.duplicate("ProjectorPanel")

        mat = random.randint(6, 8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        r = random.gauss(1, 0.05)
        self.scale('x', r)
        r = random.gauss(1, 0.03)
        self.scale('z', r)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.55)
        self.scale('y', 0.55)
        self.scale('z', 0.55)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')
        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'

        y = (corner1[1] + corner2[1]) / 2
        if orientation == 'R':
            x = corner1[0] - (0.5 * 0.35)
            duplicatedMesh.rotation_axis_angle = (math.radians(0), 0, 0, 1)
        else:
            x = corner1[0] + (0.5 * 0.35)
            duplicatedMesh.rotation_axis_angle = (math.radians(180), 0, 0, 1)
        duplicatedMesh.location = (x, y, wallHeight / 2)
        print("Generating projector panel on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return duplicatedMesh

    def putReadingLamp(self, deskBounds, deskHeight, deskOrientation):
        duplicatedMesh = self.duplicate("ReadingLamp")
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        r = random.uniform(0, 1)
        if r > 0.5:
            if deskOrientation == 90:
                duplicatedMesh.location = (deskBounds[1][0] - (2.2 * 0.35), deskBounds[1][1] - (1.5 * 0.35), deskHeight)
                duplicatedMesh.rotation_axis_angle = (math.radians(90), 0, 0, 1)
            if deskOrientation == 270:
                duplicatedMesh.location = (deskBounds[3][0] - (2.2 * 0.35), deskBounds[3][1] + (1.5 * 0.35), deskHeight)
                duplicatedMesh.rotation_axis_angle = (math.radians(90), 0, 0, 1)
        else:
            if deskOrientation == 90:
                duplicatedMesh.location = (deskBounds[0][0] + (2.2 * 0.35), deskBounds[0][1] - (1.5 * 0.35), deskHeight)
                duplicatedMesh.rotation_axis_angle = (math.radians(-90), 0, 0, 1)
            if deskOrientation == 270:
                duplicatedMesh.location = (deskBounds[2][0] + (2.2 * 0.35), deskBounds[2][1] + (1.5 * 0.35), deskHeight)
                duplicatedMesh.rotation_axis_angle = (math.radians(270), 0, 0, 1)

        print("Generating reading lamp on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return [r, duplicatedMesh]

    def putMonitor(self, deskBounds, deskHeight, deskOrientation):
        duplicatedMesh = self.duplicate("Monitor")

        screen = [18, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        #bm.faces.ensure_lookup_table()
        for i in screen:
            bm.faces[i].select = True

        # width-------------------
        r = random.gauss(1.1, 0.2)
        self.scale('y', r)
        # height--------------------
        r = random.gauss(1, 0.1)
        self.scale('z', r)
        # orientation-------------
        r = random.gauss(0.03, 0.15)
        self.rotate('y', r)

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'

        if deskOrientation == 90:
            duplicatedMesh.location = ((deskBounds[0][0] + deskBounds[1][0]) / 2, deskBounds[1][1] - (1 * 0.35), deskHeight)
            duplicatedMesh.rotation_axis_angle = (math.radians(180), 0, 0, 1)
        if deskOrientation == 270:
            duplicatedMesh.location = ((deskBounds[0][0] + deskBounds[1][0]) / 2, deskBounds[2][1] + (1 * 0.35), deskHeight)
            duplicatedMesh.rotation_axis_angle = (math.radians(0), 0, 0, 1)

        print("Generating monitor on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return duplicatedMesh

    def putKeyboardAndMouse(self, deskBounds, deskHeight, deskOrientation):
        l = []
        duplicatedMesh = self.duplicate("Keyboard")
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        if deskOrientation == 90:
            duplicatedMesh.location = (((deskBounds[0][0] + deskBounds[1][0]) / 2) - (0.2 * 0.35), deskBounds[1][1] - (0.73 * 0.35), deskHeight)
            duplicatedMesh.rotation_axis_angle = (math.radians(0), 0, 0, 1)
        if deskOrientation == 270:
            duplicatedMesh.location = (((deskBounds[0][0] + deskBounds[1][0]) / 2) + (0.2 * 0.35), deskBounds[2][1] + (0.73 * 0.35), deskHeight)
            duplicatedMesh.rotation_axis_angle = (math.radians(180), 0, 0, 1)
        print("Generating keyboard on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True
        l.append(duplicatedMesh)

        duplicatedMesh2 = self.duplicate("Mouse")
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh2.rotation_mode = 'AXIS_ANGLE'
        if deskOrientation == 90:
            duplicatedMesh2.location = (((deskBounds[0][0] + deskBounds[1][0]) / 2) - (duplicatedMesh.dimensions[0] / 2) - (0.5 * 0.35), deskBounds[1][1] - (0.58 * 0.35), deskHeight)
            duplicatedMesh2.rotation_axis_angle = (math.radians(270), 0, 0, 1)
        if deskOrientation == 270:
            duplicatedMesh2.location = (((deskBounds[0][0] + deskBounds[1][0]) / 2) + (duplicatedMesh.dimensions[0] / 2) + (0.5 * 0.35), deskBounds[2][1] + (0.58 * 0.35), deskHeight)
            duplicatedMesh2.rotation_axis_angle = (math.radians(90), 0, 0, 1)
        print("Generating mouse on ", tuple(duplicatedMesh.location))

        duplicatedMesh2.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True
        l.append(duplicatedMesh2)
        return l

    def putClothHanger(self, bounds, previousBounds):
        duplicatedMesh = self.duplicate("ClothHanger")

        mat = random.randint(6,8)
        duplicatedMesh.data.materials[0] = bpy.data.materials[mat]
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        #bm.faces.ensure_lookup_table()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        if bounds[2][0] == previousBounds[2][0]:
            duplicatedMesh.location = (bounds[3][0] - (2 * 0.35), bounds[3][1] + (1.5 * 0.35), 0)
        else:
            duplicatedMesh.location = (bounds[2][0] + (2 * 0.35), bounds[2][1] + (1.5 * 0.35), 0)
        print("Generating cloth hanger on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return duplicatedMesh

    def putSink(self, bounds):
        duplicatedMesh = self.duplicate("Sink")
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        if random.uniform(0,1) > 0.5:
            duplicatedMesh.location = (bounds[0][0] + 0.9, (bounds[0][1] + bounds[2][1]) / 2 - random.uniform(1,3), 2)
            duplicatedMesh.rotation_axis_angle = (math.radians(90), 0, 0, 1)
        else:
            duplicatedMesh.location = (bounds[1][0] - 0.9, (bounds[0][1] + bounds[2][1]) / 2 - random.uniform(1,3), 2)
            duplicatedMesh.rotation_axis_angle = (math.radians(270), 0, 0, 1)
        print("Generating sink on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return duplicatedMesh

    def putToilet(self, bounds):
        duplicatedMesh = self.duplicate("Toilet")
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh.rotation_mode = 'AXIS_ANGLE'
        duplicatedMesh.location = ((bounds[1][0] + bounds[0][0]) / 2 + 0, bounds[1][1] - 0.8, 0)
        duplicatedMesh.rotation_axis_angle = (math.radians(0), 0, 0, 1)
        print("Generating toilet on ", tuple(duplicatedMesh.location))

        duplicatedMesh.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        duplicatedMesh2 = self.duplicate("Toilet")
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh2.rotation_mode = 'AXIS_ANGLE'
        duplicatedMesh2.location = ((bounds[1][0] + bounds[0][0]) / 2 + (bounds[1][0] - bounds[0][0]) / 3, bounds[1][1] - 0.8, 0)
        duplicatedMesh2.rotation_axis_angle = (math.radians(0), 0, 0, 1)
        print("Generating toilet on ", tuple(duplicatedMesh2.location))

        duplicatedMesh2.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        duplicatedMesh3 = self.duplicate("Toilet")
        self.scale('x', 0.35)
        self.scale('y', 0.35)
        self.scale('z', 0.35)
        bpy.ops.object.move_to_layer(layers=(
            True, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
            False,
            False, False, False, False))
        bpy.ops.object.select_all(action='DESELECT')

        duplicatedMesh3.rotation_mode = 'AXIS_ANGLE'
        duplicatedMesh3.location = (
        (bounds[1][0] + bounds[0][0]) / 2 - (bounds[1][0] - bounds[0][0]) / 3, bounds[1][1] - 0.8, 0)
        duplicatedMesh3.rotation_axis_angle = (math.radians(0), 0, 0, 1)
        print("Generating toilet on ", tuple(duplicatedMesh3.location))

        duplicatedMesh3.select = False
        bpy.context.scene.objects.active = None
        bpy.context.scene.layers[1] = False
        bpy.context.scene.layers[0] = True

        return [duplicatedMesh, duplicatedMesh2, duplicatedMesh3]
