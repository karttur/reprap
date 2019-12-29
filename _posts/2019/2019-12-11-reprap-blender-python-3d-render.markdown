---
layout: post
title: Python scripting in Blender
categories: blog
excerpt: "How to control Blender through Python scripting"
tags:
  - reprap
  - software
  - Blender
  - Meshmixer
  - repetier-host
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-11 11:27'
modified: '2019-12-11 11:27'
comments: true
share: true
---

## Introduction

I use <span class='app'>Blender</span> for creating 3D models that can later be printed as objects. The 3D models can be created interactively using the <span class='app'>Blender</span> GUI, but I create most of my objects using Python scripting for controlling <span class='app'>Blender</span>.

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

Then run the script from the menu below the text editor window, illustrated in the figure below. You should then get the cylinder as shown in the canvas area on the figure.

<figure>
<img src="../../images/blender-python03.png">
<figcaption> Blender GUI, run python script.</figcaption>
</figure>
