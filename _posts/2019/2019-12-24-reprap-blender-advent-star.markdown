---
layout: post
title: Spare part for my adventsstjärna
categories: blender-python
excerpt: "Design spare part for my adventsstjärna."
tags:
  - reprap
  - Blender
  - python
  - advent
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-24 11:27'
modified: '2019-12-24 11:27'
comments: true
share: true
---

## Introduction

This post just contains the code for creating a spare part from my "adventesstjärna".

## Start Blender with clean view

Start <span class='app'>Blender</span> and [open the scripting view as described in an earlier post](../../setup/reprap-blender-python-3d-render/). Copy the script below the figure to the python text editor. Then just run the script as described in the [same post linked above](../../setup/reprap-blender-python-3d-render/).

<figure>
<img src="../../images/blender-3d-model-adventstar-holder.png">
<figcaption> STL model generated in blender by the Python code below. </figcaption>
</figure>

```
import bpy
import mathutils
import sys
from math import radians,sin,asin,cos,atan,tan,sqrt

#from xml.dom import minidom

def CleanOb(ob):
    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
    return

def UnionObs(primOb,secOb):
    bpy.context.scene.objects.active = primOb
    boo = primOb.modifiers.new('BooU', 'BOOLEAN')
    boo.object = secOb
    boo.operation = 'UNION'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BooU")
    bpy.context.scene.objects.unlink(secOb)
    CleanOb(primOb)

def DiffObs(primOb,secOb):
    bpy.context.scene.objects.active = primOb
    boo = primOb.modifiers.new('BooD', 'BOOLEAN')
    boo.object = secOb
    boo.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BooD")
    bpy.context.scene.objects.unlink(secOb)
    CleanOb(primOb)

def IntersectObs(primOb,secOb):
    bpy.context.scene.objects.active = primOb
    boo = primOb.modifiers.new('BooI', 'BOOLEAN')
    boo.object = secOb
    boo.operation = 'INTERSECT'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BooI")
    bpy.context.scene.objects.unlink(secOb)
    CleanOb(primOb)

##### Set fixed parameters
# defualt rotation
rotation = (0,0,0)

#create a clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

#set units
bpy.types.UnitSettings.system = 'METRIC'
bpy.types.UnitSettings.scale_length = 0.001

#set scene units
scn=bpy.context.scene

#bpy.data.scenes[0].UnitSettings.system = 'METRIC'
bpy.data.scenes[0].unit_settings.scale_length = 0.001

name = "prism"
meshes = bpy.data.meshes
scn = bpy.context.scene

#points = [ [-1,-1,-1],[-1,0,1],[-1,1,-1],[1,-1,-1],[1,0,1],[1,1,-1] ]
points = [ [-3,-1.6,0],[-3,0,2],[-3,1.6,0],[3,-1.6,0],[3,0,2],[3,1.6,0] ]
faces = [ [4,5,2],[1,0,3],[2,5,3],[4,3,5],[1,2,0],[1,4,2],[4,1,3],[0,2,3] ]

shape_vertices = []
for p in points:
    shape_vertices.append ( mathutils.Vector((p[0],p[1],p[2])) )

new_mesh = bpy.data.meshes.new ( name + "_mesh" )
new_mesh.from_pydata ( shape_vertices, [], faces )
new_mesh.update()

print_ob = bpy.data.objects.new ( name, new_mesh )
scn.objects.link ( print_ob )

#2nd mesh

points = [ [-2.5,-2,0],[-2.5,0,2.4],[-2.5,2,0],[2.5,-2,0],[2.5,0,2.4],[2.5,2,0] ]
faces = [ [4,5,2],[1,0,3],[2,5,3],[4,3,5],[1,2,0],[1,4,2],[4,1,3],[0,2,3] ]

shape_vertices = []
for p in points:
    shape_vertices.append ( mathutils.Vector((p[0],p[1],p[2])) )

new_mesh = bpy.data.meshes.new ( name + "_mesh2" )
new_mesh.from_pydata ( shape_vertices, [], faces )
new_mesh.update()

print2_ob = bpy.data.objects.new ( name, new_mesh )
scn.objects.link ( print2_ob )

#Join the two print ob
UnionObs(print_ob,print2_ob)


# Add a cube
#create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=(0,2,2), rotation=(radians(45),0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(2, 2, 2))

DiffObs(print_ob, cutter_ob)

# Add another cube
#create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=(0,-2,2), rotation=(radians(45),0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(2, 2, 2))

DiffObs(print_ob, cutter_ob)

# Add 3rd cube
#create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=(-2.5,-2,2), rotation=(radians(53),0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(0.3, 2, 2))

DiffObs(print_ob, cutter_ob)

# Add 4th cube
#create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=(2.5,-2,2), rotation=(radians(53),0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(0.3, 2, 2))

DiffObs(print_ob, cutter_ob)

# Add 5th cube
#create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=(2.5,2,2), rotation=(radians(37),0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(0.3, 2, 2))

DiffObs(print_ob, cutter_ob)

# Add 7th cube
#create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=(-2.5,2,2), rotation=(radians(37),0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(0.3, 2, 2))

DiffObs(print_ob, cutter_ob)

# Add 6th cube
#create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=(0,0,2.5), rotation=(0,0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(6, 6, 1))

DiffObs(print_ob, cutter_ob)

# Add cylinder
#create the platform square and rescale it
bpy.ops.mesh.primitive_cylinder_add( radius=1, location=(0,0.75,1), rotation=(0,0,0))
cutter_ob = bpy.context.object
bpy.ops.transform.resize(value=(0.6, 0.6, 2))

DiffObs(print_ob, cutter_ob)

FP = "/Users/thomasgumbricht/docs-local/STL_models/2019/advent-light.ply"
bpy.ops.export_mesh.ply(filepath=FP)
```
