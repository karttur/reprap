---
layout: post
title: Python scripting in Blender
categories: setup
excerpt: "How to control Blender through Python scripting"
tags:
  - reprap
  - Blender
  - Scripting
  - Python
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-11 11:27'
modified: '2019-12-11 11:27'
comments: true
share: true
---

## Introduction

I use <span class='app'>Blender</span> for creating 3D models that can later be printed as objects. The 3D models can be created interactively using the <span class='app'>Blender</span> GUI, but I create most of my objects using Python scripting for controlling <span class='app'>Blender</span>. The two next posts introduces [interactive modeling](../reprap-blender-rudder-part1) and [modeling using python scripting](../reprap-blender-rudder-part2). This post covers the setup of <span class='app'>Blender</span> for python scripting.

## Prerequisites

You need to install a version of <span class='app'>Blender</span> that can be used for Python scripting, detailed in the [previous](../reprap-software/) post.

## Blender

Start <span class='app'>Blender</span> (in my case Blender276.app).

To run <span class='app'>Blender</span> using Python you have to change the _Screen Layout_ from _Default_ to _Scripting_, as shown in the image below.

<figure>
<img src="../../images/blender-python01.png">
<figcaption> Blender GUI, change screen layout from Default to Scripting.</figcaption>
</figure>

The GUI changes and the canvas area gets divided into a script and a canvas area. Below the empty script area, click the _New_ option and then _Create a new text data block_. Illustrated in the figure below.

<figure>
<img src="../../images/blender-python02.png">
<figcaption> Blender GUI, initialise text scripting.</figcaption>
</figure>

Now you can write your Python code in the text editor area. For the example figure below, add the following script:

```
'''
Created on 14 feb 2012

@author: thomasg
import scipy

'''
import sys

import bpy

from math import radians,sin,cos

#create a clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
#scaleF is for converting all measures
scaleF = 0.5

radiusOut = 16.4
depthOut = 40
#locationOut = (radiusOut*scaleF,radiusOut*scaleF,depthOut*scaleF/2)
locationOut = (0,0,depthOut*scaleF/2)
rotation = (0,0,0)
bpy.ops.mesh.primitive_cylinder_add(radius=radiusOut*scaleF, depth=depthOut*scaleF, location=locationOut, rotation=rotation)
outcyl_ob = bpy.context.object
```

Then run the script from the menu below the text editor window, illustrated in the figure below.

<span class='menu'>text -> Run Script</span>

You should then get the cylinder as shown in the canvas area on the figure.

<figure>
<img src="../../images/blender-python03.png">
<figcaption> Blender GUI, run python script.</figcaption>
</figure>

## Default Python code

When I design and create my own 3D objects, I primarily use basic shapes (mesh, cube, circle, cylinder, cone, torus etc) and then reshape these using scripting. The moulding of the basic shapes into the shapes I want is done individually. But then I often use the moulded objects for either cutting out pieces from or adding to, existing objects. To facilitate that I have defined four functions: _CleanOb_, _UnionObs_, _DiffObs_ and _IntersectObs_. I thus tend to start every design with the same basic script:

```
import bpy
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
```
