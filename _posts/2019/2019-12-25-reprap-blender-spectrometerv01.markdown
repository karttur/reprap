---
layout: post
title: Design spectrometer v 01
categories: spectromodel
excerpt: "Design spectrometer."
tags:
  - reprap
  - Blender
  - python
  - advent
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-25 11:27'
modified: '2019-12-25 11:27'
comments: true
share: true
---

## Introduction



## Start Blender with clean view

Start <span class='app'>Blender</span> and [open the scripting view as described in an earlier post](../reprap-blender-python-3d-render/). Copy the following script to the python text editor. Then just run the script as described in the [same post linked above](../reprap-blender-python-3d-render/).

```
import bpy
import mathutils
import sys
from math import radians,sin,asin,cos,atan,tan,sqrt
from xml.dom import minidom

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
### defualt rotation
rotation = (0,0,0)

### create a clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

### set units
bpy.types.UnitSettings.system = 'METRIC'
bpy.types.UnitSettings.scale_length = 0.001

### set scene units
scn=bpy.context.scene

### Set constants

rotation = (0,0,0)

##### Get and set all parameters

### link to xml file ith all definitions
xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/spectrodim_2019_v01.xml'
# xmlFN = '/Applications/spectrodim_2019_v01.xml'

### Parse xml file
dom = minidom.parse(xmlFN)

## Set global parameters

boxTag = dom.getElementsByTagName('box')
boxW = float(boxTag[0].getAttribute('W'))/2
boxL = float(boxTag[0].getAttribute('L'))/2
boxWallT = float(boxTag[0].getAttribute('wallT'))
boxRoofT = float(boxTag[0].getAttribute('roofT'))
boxFloorT = float(boxTag[0].getAttribute('floorT'))
boxCornerR = float(boxTag[0].getAttribute('cornerradius'))

xmax = boxW-boxWallT
xmin = -boxW+boxWallT
ymax = boxL-boxWallT
ymin = -boxL+boxWallT

topTag = dom.getElementsByTagName('top')
topH = float(topTag[0].getAttribute('H'))
topInnerRim = float(topTag[0].getAttribute('innerrim'))
topRimHeight = float(topTag[0].getAttribute('rimheight'))

## get the top

bottomTag = dom.getElementsByTagName('bottom')
bottomH = float(bottomTag[0].getAttribute('H'))
bottomOuterRim = float(bottomTag[0].getAttribute('outerrim'))
bottomRimHeight = float(bottomTag[0].getAttribute('rimheight'))

## Create the platform (bottom or top is the amse except for wallT

# Set platform position
platformBoxPos = (0,0,boxRoofT/2)

## create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=platformBoxPos, rotation=rotation)
platform_ob = bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxW-boxCornerR, boxL, boxRoofT/2))

## create the platform square and rescale it
bpy.ops.mesh.primitive_cube_add( radius=1, location=platformBoxPos, rotation=rotation)
platform2_ob = bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxW, boxL-boxCornerR, boxRoofT/2))

## Union the two platformpieces

UnionObs(platform_ob, platform2_ob)

#Loop over corners to add the rounded edges

ulpos = (boxW-boxCornerR,boxL-boxCornerR,boxFloorT/2)
bpy.ops.mesh.primitive_cylinder_add( radius=1, location=ulpos, rotation=rotation)
corner_ob= bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxCornerR, boxCornerR, boxRoofT/2))
UnionObs(platform_ob, corner_ob)

urpos = (boxW-boxCornerR,-boxL+boxCornerR,boxFloorT/2)
bpy.ops.mesh.primitive_cylinder_add( radius=1, location=urpos, rotation=rotation)
corner_ob= bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxCornerR, boxCornerR, boxRoofT/2))
UnionObs(platform_ob, corner_ob)

llpos = (-boxW+boxCornerR,-boxL+boxCornerR,boxFloorT/2)
bpy.ops.mesh.primitive_cylinder_add( radius=1, location=llpos, rotation=rotation)
corner_ob= bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxCornerR, boxCornerR, boxRoofT/2))
UnionObs(platform_ob, corner_ob)

lrpos = (-boxW+boxCornerR,boxL-boxCornerR,boxFloorT/2)
bpy.ops.mesh.primitive_cylinder_add( radius=1, location=lrpos, rotation=rotation)
corner_ob= bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxCornerR, boxCornerR, boxRoofT/2))
UnionObs(platform_ob, corner_ob)

##### Platform ready - same for bottom and top

##### Make 4 copies of the platform

# Copy the platform - the only object so far
bpy.ops.object.select_all(action='SELECT')

#Create two copies, they will beoce the inner and outerwalls
bpy.ops.object.duplicate_move()
outerwall_ob = bpy.context.object

bpy.ops.object.duplicate_move()
innerwall_ob = bpy.context.object

bpy.ops.object.duplicate_move()
outerrim_ob = bpy.context.object

bpy.ops.object.duplicate_move()
innerrim_ob = bpy.context.object

#scale the outerwall object
#bpy.ops.transform.resize(value=(1, 1, topH))

zfac = topH/boxRoofT

#select and scale the outerwall
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.objects.active = outerwall_ob
outerwall_ob.select = True
bpy.ops.transform.resize(value=(1, 1, zfac))
#move the outerwall in place
bpy.ops.transform.translate(value=(0.0, 0.0, topH/2), constraint_axis=(False, False, True))

xfac = (boxW-boxWallT)/boxW
yfac = (boxL-boxWallT)/boxL
#select and scale the innerwall
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.objects.active = innerwall_ob
innerwall_ob.select = True
bpy.ops.transform.resize(value=(xfac, yfac, zfac))
#move the outerwall in place
bpy.ops.transform.translate(value=(0.0, 0.0, topH/2), constraint_axis=(False, False, True))

## Take th diff from outerwall and innewall to get the wall

DiffObs(outerwall_ob,innerwall_ob)

## Create the rim

zfac = topInnerRim/boxRoofT

#select and scale the outerrim
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.objects.active = outerrim_ob
outerrim_ob.select = True
bpy.ops.transform.resize(value=(1, 1, zfac))
#move the outerwall in place
bpy.ops.transform.translate(value=(0.0, 0.0, topH+topRimHeight/2), constraint_axis=(False, False, True))

xfac = (boxW-topInnerRim)/boxW
yfac = (boxL-topInnerRim)/boxL
#select and scale the innerwall
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.objects.active = innerrim_ob
innerrim_ob.select = True
bpy.ops.transform.resize(value=(xfac, yfac, zfac*1.25))
#move the outerwall in place
bpy.ops.transform.translate(value=(0.0, 0.0, topH+topRimHeight/2), constraint_axis=(False, False, True))

## Take th diff from outerrim and outerrim to get the rim

DiffObs(outerrim_ob,innerrim_ob)

## union the wall and the rim

UnionObs(outerwall_ob,outerrim_ob)

## Union the wall and the platform

UnionObs(platform_ob, outerwall_ob)

##### Get all the breakout boards

breakoutTag = dom.getElementsByTagName('breakouts')
## Get the square breakout boards
squares = breakoutTag[0].getElementsByTagName("square")

for square in squares:
    squid = square.getAttribute('id')
    sx = float(square.getAttribute('W'))
    sy = float(square.getAttribute('L'))
    sz = float(square.getAttribute('H'))
    px = float(square.getAttribute('centerx'))
    py = float(square.getAttribute('centery'))
    pz = float(square.getAttribute('centerz'))
    rx = float(square.getAttribute('rotationx'))
    ry = float(square.getAttribute('rotationy'))
    rz = float(square.getAttribute('rotationz'))
    rimwidth = float(square.getAttribute('rimwidth'))
    rimheight = float(square.getAttribute('rimheight'))
    embed = float(square.getAttribute('embed'))

    if rx == ry == 0:
        #horizontal object, adjust z for embedding
        dx = sx
        dy = sy
        pz = boxFloorT+sz/2-embed
    elif rx == 90:
        dx = sx
        dy = sz
        if py < 0:
            py = ymin
        else:
            py = ymax  
        # if pz is to far down, adjust otherwise leave   
        if pz < boxFloorT+sx/2-embed:
            pz = boxFloorT+sx/2-embed
    elif ry == 90:
        #align item along x
        #set px to the xmin/xmax
        dx = sz
        if px < 0:
            px = xmin
        else:
            px = xmax  
        # if pz is to far down, adjust otherwise leave   
        if pz < boxFloorT+sx/2-embed:
            pz = boxFloorT+sx/2-embed

    if px+dx/2 > xmax+embed:
        px = xmax+embed-dx/2
    if px-dx/2 < xmin-embed:
        px = xmin-embed+dx/2

    if py+dy/2 > ymax+embed:
        py = ymax+embed-dy/2

    if py-dy/2 < ymin-embed:
        py = ymin-embed+dy/2


    position = (px,py,pz)

    if embed: #if the wall, roof or floor is going to be cut

        ## create the platform square and rescale it
        bpy.ops.mesh.primitive_cube_add( radius=1, location=position, rotation=(0,0,0) )
        del_ob = bpy.context.object
        ## Resize the platform
        bpy.ops.transform.resize(value=(sx/2, sy/2, sz/2))
        #Rotate as a postprocess

        if rx != 0:
            bpy.ops.transform.rotate(value=radians(rx), constraint_axis=(True, False, False))
        if ry != 0:
            bpy.ops.transform.rotate(value=radians(ry), constraint_axis=(False, True, False))
        if rz != 0:
            bpy.ops.transform.rotate(value=radians(rz), constraint_axis=(False, False, True))

        #Create the hole in the fram where breakout is going to sit

        DiffObs(platform_ob,del_ob)

    elif rimwidth and rimheight:
        #create rim instead of embedding in wall, floor or roof

        position = (px,py,pz)
        rotation = (radians(rx),radians(ry),radians(rz))    
        outerFrameSize = (sx/2+rimwidth, sy/2+rimwidth, rimheight/2)
        innerFrameSize = (sx/2, sy/2, rimheight/2)

        ## Createt the outer frame
        bpy.ops.mesh.primitive_cube_add( radius=1, location=position, rotation=rotation)
        frame_ob = bpy.context.object
        ## Resize the platform
        bpy.ops.transform.resize(value=(sx/2+rimwidth, sy/2+rimwidth, rimheight/2))

        ## Createt the inner removal frame
        bpy.ops.mesh.primitive_cube_add( radius=1, location=position, rotation=rotation)
        del_ob = bpy.context.object
        ## Resize the platform
        bpy.ops.transform.resize(value=(sx/2, sy/2, rimheight/2))

        ## Craete the rim
        DiffObs(frame_ob, del_ob)

        ## union the frame with the platform

        UnionObs(platform_ob, frame_ob)

    ### The breakout board is in place, loop over any associated openings

    squareholes = square.getElementsByTagName("squarehole")
    for sqh in squareholes:
        sx = float(sqh.getAttribute('W'))
        sy = float(sqh.getAttribute('L'))

        fx = float(sqh.getAttribute('fromcenterx'))
        fy = float(sqh.getAttribute('fromcentery'))

        # rotation is the same as for the mother object

        #positions is relative to the mother object center in x and y

        if rx == ry == 0:
            #horizontal object, adjust z for embedding
            position = (position[0]+fx, position[1]+fy,boxFloorT/2)
        elif rx == 90:

            position = (position[0]+fy, boxL-(boxWallT/2), position[2])

        elif ry == 90:
            position = (boxW-(boxWallT/2), position[1]+fy, position[2]+fx)

        bpy.ops.mesh.primitive_cube_add( radius=1, location=position, rotation=rotation)
        del_ob = bpy.context.object
        ## Resize the platform
        bpy.ops.transform.resize(value=(sx/2, sy/2, boxFloorT))

        DiffObs(platform_ob, del_ob)

    roundholes = square.getElementsByTagName("roundhole")
    for sqh in roundholes:
        sx = float(sqh.getAttribute('W'))
        sy = float(sqh.getAttribute('L'))

        fx = float(sqh.getAttribute('fromcenterx'))
        fy = float(sqh.getAttribute('fromcentery'))

        # rotation is the same as for the mother object

        #positions is relative to the mother object center in x and y

        if rx == ry == 0:
            #horizontal object, adjust z for embedding
            position = (position[0]+fx, position[1]+fy,boxFloorT/2)
        elif rx == 90:

            position = (position[0]+fy, boxL-(boxWallT/2), position[2])

        elif ry == 90:
            position = (boxW-(boxWallT/2), position[1]+fy, position[2]+fx)

        bpy.ops.mesh.primitive_cylinder_add( radius=sx, depth = boxWallT*1.05, location=position, rotation=rotation)
        #Rotate as a postprocess
        del_ob = bpy.context.object
        if rx != 0:
            bpy.ops.transform.rotate(value=radians(rx), constraint_axis=(True, False, False))
        if ry != 0:
            bpy.ops.transform.rotate(value=radians(ry), constraint_axis=(False, True, False))
        if rz != 0:
            bpy.ops.transform.rotate(value=radians(rz), constraint_axis=(False, False, True))

        DiffObs(platform_ob, del_ob)

FP = "/Users/thomasgumbricht/docs-local/STL_models/2019/test_20200103.ply"
bpy.ops.export_mesh.ply(filepath=FP)     
```
