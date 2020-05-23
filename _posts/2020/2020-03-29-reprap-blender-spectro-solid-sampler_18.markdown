---
layout: post
title: Design spectrometer v 18
categories: spectromodel
excerpt: "Design spectrometer."
tags:
  - reprap
  - Blender
  - python
  - spetrometer
  - solid sampler
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2020-03-29  11:27'
modified: '2020-03-29  11:27'
comments: true
share: true
---

## Introduction



## Start Blender with clean view

Start <span class='app'>Blender</span> and [open the scripting view as described in an earlier post](../reprap-blender-python-3d-render/). Copy the following script to the python text editor. Then just run the script as described in the [same post linked above](../reprap-blender-python-3d-render/).

```
"""
Python script for running inside Blender

Written by: Thomas Gumbricht

Version: 1.11

Updated: 20200106

"""

##### Imports

import bpy
import mathutils
import sys
from math import radians,sin,asin,cos,atan,tan,sqrt
from xml.dom import minidom

#####

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/spectro-solid-holder_20200329_v18.xml'
#xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/spectro-solid-holder_20200329_v18.xml'
#xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/spectro-solid_20200328_v18.xml'

#xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/spectro-solid-lock_20200329_v18.xml'
###### Common functions

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

def ScaleMoveVertically(ob, xfac, yfac, zfac, zpos):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = ob
    ob.select = True
    bpy.ops.transform.resize(value=(xfac, yfac, zfac))
    #move the outerwall in place
    bpy.ops.transform.translate(value=(0.0, 0.0, zpos), constraint_axis=(False, False, True))

def FixRotations(px,py,pz,sx,sy,sz,rx,ry,rz,inside):
    if rx == ry == 0:
        # horizontal object, adjust z for embedding
        dx = sx
        dy = sy
        dz = sz
        if pz == 0 and inside:
            pz = boxFloorT+sz/2-embed
            print ('altering pz from 0 to', pz)
        elif not inside:
            pass
            #pz = 0
    elif rx == 90:
        # Rotated around the x axis
        dx = sx
        dy = sz
        dz = sy
        # move to side wall
        if inside:
            if py < 0:
                py = ymin
            else:
                py = ymax
            # if pz is too far down, adjust otherwise leave   
            if pz < boxFloorT+dz/2-embed:
                pz = boxFloorT+dz/2-embed
        else:
            pass
            #if py < 0:
            #    py = ymin-boxWallT
            #else:
            #    py = ymax+boxWallT
            #if pz < 0:
            #    pz = 0


    elif ry == 90:
        # Rotated around the y axis
        dx = sz
        dy = sy
        dz = sx
        if inside:
            if px < 0:
                px = xmin
            else:
                pass
                px = xmax  
            # if pz is to far down, adjust otherwise leave   
            if pz < boxFloorT+dz/2-embed:
                pz = boxFloorT+dz/2-embed
        else:
            pass
            #if px < 0:
            #    px = xmin-boxWallT
            #else:
            #    px = xmax

    #Check that the item is inside the box
    if inside:
        if px+dx/2 > xmax+embed:
            px = xmax+embed-dx/2
        if px-dx/2 < xmin-embed:
            px = xmin-embed+dx/2

        if py+dy/2 > ymax+embed:
            py = ymax+embed-dy/2

        if py-dy/2 < ymin-embed:
            py = ymin-embed+dy/2

    return (dx,dy,dz,px,py,pz)

def SizeRotateItem(sxhalf,syhalf,szhalf,rx,ry,rz):
    ### resize
    bpy.ops.transform.resize(value=(sxhalf,syhalf,szhalf))

    #Rotate as a postprocess
    if rx != 0:     
        bpy.ops.transform.rotate(value=radians(rx), constraint_axis=(True, False, False))
    if ry != 0:
        bpy.ops.transform.rotate(value=radians(ry), constraint_axis=(False, True, False))
    if rz != 0:
        bpy.ops.transform.rotate(value=radians(rz), constraint_axis=(False, False, True))

    return bpy.context.object

def CreateCube(position,sxhalf,syhalf,szhalf,rx,ry,rz=0):

    bpy.ops.mesh.primitive_cube_add( radius=1, location=position, rotation=(0,0,0) )
    return SizeRotateItem(sxhalf,syhalf,szhalf,rx,ry,rz)

def CreateCylinder(position, depth, sxhalf, syhalf, szhalf, rx, ry, rz=0):

    bpy.ops.mesh.primitive_cylinder_add( radius=1, depth=depth, location=position, rotation=(0,0,0) )
    #bpy.ops.mesh.primitive_cylinder_add( radius=1, location=position, rotation=(0,0,0) )

    return SizeRotateItem(sxhalf,syhalf,szhalf,rx,ry,rz)

def CreateText(storlek, position, rotation, imprint, depth=1, font='arial', fontsize=16):
	#create the text object
    bpy.ops.object.text_add( location=position)
    mytext = bpy.data.objects["Text"]
    mytext.data.body = imprint
    #set some stuff up
    #mytext.data.align_x = "CENTER"
    #mytext.data.align_y = "BOTTOM"
    mytext.data.extrude = 1
    #fnt = bpy.data.fonts.load(font_loc)              #font loading works
    #mytext.data.font = fnt
    bpy.context.scene.objects.active = mytext   # make sure my Text object is correctly selected
    mytext.select = True
    bpy.ops.object.convert(target="MESH") # Convert to mesh

    SizeRotateItem(storlek[0], storlek[1], storlek[2], rotation[0], rotation[1], rotation[2])

    return bpy.context.object

# Define if this is the lock or the main box
lock = False

##### Initial parameters and defintions

### defualt rotation
rotation = (0,0,0)

### create a clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select = True
    else:
        obj.select = False
    bpy.ops.object.delete()

for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)

for block in bpy.data.materials:
    if block.users == 0:
        bpy.data.materials.remove(block)

for block in bpy.data.textures:
    if block.users == 0:
        bpy.data.textures.remove(block)

for block in bpy.data.objects:
    if block.users == 0:
        bpy.data.objects.remove(block)

for block in bpy.data.images:
    if block.users == 0:
        bpy.data.images.remove(block)

### set distance units
bpy.types.UnitSettings.system = 'METRIC'
bpy.types.UnitSettings.scale_length = 0.001

### set the scene
scn=bpy.context.scene

##### Read xml file and some of the initial parameters

### Parse xml file
dom = minidom.parse(xmlFN)

### Box paramters
outputTag = dom.getElementsByTagName('output')
doPly = int(outputTag[0].getAttribute('ply'))
doStl= int(outputTag[0].getAttribute('stl'))
doObj = int(outputTag[0].getAttribute('obj'))
FPNnoExt = outputTag[0].childNodes[0].nodeValue.strip()

boxTag = dom.getElementsByTagName('box')
boxW = float(boxTag[0].getAttribute('W'))/2
boxL = float(boxTag[0].getAttribute('L'))/2
boxH = float(boxTag[0].getAttribute('H'))

boxWallT = float(boxTag[0].getAttribute('wallT'))
boxFloorT = float(boxTag[0].getAttribute('floorT'))
boxCornerR = float(boxTag[0].getAttribute('cornerradius'))

boxInnerRim = float(boxTag[0].getAttribute('innerrim'))
boxOuterRim = float(boxTag[0].getAttribute('outerrim'))
boxRimHeight = float(boxTag[0].getAttribute('rimheight'))

### Calculate maximum dimensions

xmax = boxW-boxWallT
xmin = -boxW+boxWallT
ymax = boxL-boxWallT
ymin = -boxL+boxWallT

### Create the platform (bottom or top is the same

# Set platform position
platformBoxPos = (0,0,boxFloorT/2)

### create the first platform square and resize it
bpy.ops.mesh.primitive_cube_add( radius=1, location=platformBoxPos, rotation=rotation)
platform_ob = bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxW-boxCornerR, boxL, boxFloorT/2))

### create the second platform square and resize it
bpy.ops.mesh.primitive_cube_add( radius=1, location=platformBoxPos, rotation=rotation)
platform2_ob = bpy.context.object
## Resize the platform
bpy.ops.transform.resize(value=(boxW, boxL-boxCornerR, boxFloorT/2))

## Union the two platform pieces
UnionObs(platform_ob, platform2_ob)

### Loop over corners to add the rounded edges

cornerPosL = [(boxW-boxCornerR,boxL-boxCornerR,boxFloorT/2),
              (boxW-boxCornerR,-boxL+boxCornerR,boxFloorT/2),
              (-boxW+boxCornerR,-boxL+boxCornerR,boxFloorT/2),
              (-boxW+boxCornerR,boxL-boxCornerR,boxFloorT/2)]

for p in cornerPosL:
    bpy.ops.mesh.primitive_cylinder_add( radius=1, location=p, rotation=rotation)
    corner_ob= bpy.context.object
    ## Resize the corner cylinder
    bpy.ops.transform.resize(value=(boxCornerR, boxCornerR, boxFloorT/2))
    ## Union the paltform and the corner
    UnionObs(platform_ob, corner_ob)

##### Platform ready

##### Make copies of the platform, for the outher and inner walls and the outer and innter rimes

# Copy the platform - the only object so far
bpy.ops.object.select_all(action='SELECT')

#
xfac = yfac = 1

# Craete the inner room
bpy.ops.object.duplicate_move()
innerwall_ob = bpy.context.object

##### Create rim if requested

if ( boxInnerRim or boxOuterRim ) and boxRimHeight:
    # Set z-fac for rim
    zfac = boxRimHeight/boxFloorT

    if boxOuterRim: # This creates an outer rime
        xfac = yfac = 1

        bpy.ops.object.duplicate_move()
        rim_ob = bpy.context.object

        # select and scale the outerwall
        ScaleMoveVertically(rim_ob, xfac, yfac, zfac, boxH-boxRimHeight/2)

        # Create the eraser object

        bpy.ops.object.duplicate_move()
        rimdel_ob = bpy.context.object

        xfac = yfac = (boxW-boxOuterRim)/boxW

        ScaleMoveVertically(rimdel_ob, xfac, yfac, 2, 0)

        DiffObs(rim_ob, rimdel_ob)

    else:
        xfac = yfac = 1

        bpy.ops.object.duplicate_move()
        rim_ob = bpy.context.object

        # select and scale the outerwall
        ScaleMoveVertically(rim_ob, xfac, yfac, zfac, boxH-1.45*boxRimHeight)
        #ScaleMoveVertically(rim_ob, xfac, yfac, zfac, 1)

        # Create the eraser object

        bpy.ops.object.duplicate_move()
        rimdel_ob = bpy.context.object

        negative_rim = boxWallT-boxInnerRim

        xfac = yfac = (boxW - negative_rim)/boxW

        ScaleMoveVertically(rimdel_ob, xfac, yfac, 2, 0)

        DiffObs(rim_ob, rimdel_ob)

# All scaling in x and y of the platfrom is at unity
xfac = yfac = 1

#bpy.ops.object.duplicate_move()
#innerwall_ob = bpy.context.object

#set the z scale factor

zfac = boxH/boxFloorT

# select and scale the outerwall

ScaleMoveVertically(platform_ob, xfac, yfac, zfac, boxH/2-boxFloorT/2)

# select and scale the innerwall
xfac = (boxW-boxWallT)/boxW
yfac = (boxL-boxWallT)/boxL

ScaleMoveVertically(innerwall_ob, xfac, yfac, zfac, boxFloorT/2+(boxH/2))

## Take the diff from outerwall and innewall to get the wall
DiffObs(platform_ob,innerwall_ob)

##### Box outline ready

if boxOuterRim and boxRimHeight:
    UnionObs(platform_ob,rim_ob)

if boxInnerRim and boxRimHeight:
    DiffObs(platform_ob,rim_ob)

##### Get all the breakout boards

structTag = dom.getElementsByTagName('structures')
## Get the square breakout boards
items = structTag[0].getElementsByTagName("item")

for item in items:

    itemid = item.getAttribute('id')
    baseshape = item.getAttribute('baseshape')
    inside = int(item.getAttribute('inside'))
    sx = float(item.getAttribute('W'))
    sy = float(item.getAttribute('L'))
    sz = float(item.getAttribute('H'))
    sxx = float(item.getAttribute('W'))
    syy = float(item.getAttribute('L'))
    szz = float(item.getAttribute('H'))
    px = float(item.getAttribute('centerx'))
    py = float(item.getAttribute('centery'))
    pz = float(item.getAttribute('centerz'))
    rx = float(item.getAttribute('rotationx'))
    ry = float(item.getAttribute('rotationy'))
    rz = float(item.getAttribute('rotationz'))
    rimwidth = float(item.getAttribute('rimwidth'))
    rimheight = float(item.getAttribute('rimheight'))
    embed = float(item.getAttribute('embed'))

    ### Fix the rotation, only rotations in x and y are valid, rotation in z is simply changing W and L

    dx,dy,dz,px,py,pz = FixRotations(px,py,pz,sx,sy,sz,rx,ry,rz,inside)

    ### Set the position       
    position = (px,py,pz)

    if embed: #if the wall, roof or floor is going to be carved out to fir the item
        ## create the platform square and rescale it
        if baseshape == 'cube':
            del_ob = CreateCube(position,sx/2,sy/2,sz/2,rx,ry)
        elif baseshape == 'cylinder':     
            del_ob = CreateCylinder(position, 1, sx/2,sy/2,sz/2,rx,ry)
        elif baseshape == 'text':
            text = item.getAttribute('text')
            textT = text.split(';')
            newText = textT[0]
            for t in range(1,len(textT)):
                newText = '%s\n%s' % (newText, textT[t])  

            storlek = (sxx, syy, szz)
            rotate = (rx,ry,rz)
            del_ob = CreateText(storlek, position, rotate, newText)

        #Cut out the material for the item site inside the box
        DiffObs(platform_ob,del_ob)

    if rimwidth or rimheight:
        if inside:
            position = (px,py,boxFloorT+rimheight/2)
        else:
            position = (px,py,rimheight/2)


        ## Create frame
        if baseshape == 'cube':
            if not rimwidth:
                del_ob = CreateCube(position,sx/2,sy/2,rimheight/2,rx,ry, rz)
                DiffObs(platform_ob, del_ob)
            # Create outer frame
            if sx * sy != 0: #no width or length
                frame_ob = CreateCube(position,sx/2+rimwidth, sy/2+rimwidth, rimheight/2, rx, ry, rz)

            else:
                frame_ob = CreateCube(position,sx/2+rimwidth/2, sy/2+rimwidth/2, rimheight/2, rx, ry, rz)
            # Create inner frame
            if sx * sy != 0:
                del_ob = CreateCube(position,sx/2,sy/2,rimheight/2,rx,ry, rz)

        elif baseshape == 'cylinder':
            # Create outer frame
            if sx * sy != 0:
                frame_ob = CreateCylinder(position,sx/2+rimwidth, sy/2+rimwidth, rimheight/2,rx,ry)

            else:
                frame_ob = CreateCylinder(position,sx/2+rimwidth/2, sy/2+rimwidth/2, rimheight/2,rx,ry)

            # Create inner frame
            if sx * sy != 0:
                del_ob = CreateCylinder(position,sx/2,sy/2,rimheight/2,rx,ry)

        ## Create the frame by taken difference between frame_ob and del_ob
        if sx * sy != 0:
            DiffObs(frame_ob, del_ob)

        ## Union the frame with the platform
        UnionObs(platform_ob, frame_ob)

    ### The item, whatever it is, is in place

    ### Create all the holes associated with item (if any)

    holes = item.getElementsByTagName("hole")

    for hole in holes:
        holeshape = hole.getAttribute('holeshape')
        type = hole.getAttribute('type')
        sx = float(hole.getAttribute('W'))
        sy = float(hole.getAttribute('L'))
        #sh = float(hole.getAttribute('H'))

        fx = float(hole.getAttribute('fromcenterx'))
        fy = float(hole.getAttribute('fromcentery'))
        hrx = float(hole.getAttribute('rotationx'))
        hry = float(hole.getAttribute('rotationy'))

        hp = [position[0], position[1], position[2]]
        holepos = hp[:]
        # Rotation is the same as for the mother object

        # Positions is relative to the mother object center expressed as x and y but must be translated for rotation
        rrz = 0
        if rx == ry == 0:
            rrx = rry = rrz = 0
            #horizontal object, adjust z for embedding
            dx = sx
            dy = sy

            if type == 'opening':
                # boxFloorT*2 to fully penetrate the floor
                dz = boxFloorT*2
                holepos = (position[0]+fx, position[1]+fy, boxFloorT/2)
            if type == 'room':
                # boxFloorT*2 to fully penetrate the floor

                holepos = (position[0]+fx, position[1]+fy, position[2])

            elif type[0:4] == 'wire':
                rtyp = type.split('-')[1]
                if rtyp == 'roty':
                    rry = 90
                    dz = rimwidth+0.1
                    holepos = (position[0], position[1]+fx, position[2]+fy)
                elif rtyp == 'rotx':
                    rrx = 90
                    dz = (rimheight+0.5)
                    #the +0.5 depends on angle

                    rrx = rx
                    rry = hry
                    #rry = 10
                    holepos = (position[0]+fx, position[1]+fy, position[2]+0.5)

                    #holepos = (position[0], position[1], position[2])

                    #hole_ob = CreateCylinder(holepos, dz, dx/2, dy/2, dz, rrx, rry)
                    #hole_ob = CreateCylinder(holepos, 1, dx/2, dy/2, dz, rx, ry)

                    #hole_ob = CreateCylinder(holepos, rimwidth+0.1, dx/2, dy/2, (rimheight/2+0.1), rx, ry)

            #position = (position[0]+fx, position[1]+fy, boxFloorT/2)

        elif rx == 90:
            rrx = 90
            rry = 0
            dx = sx #size in x
            #dy = boxWallT #size in y = wall thinckness
            #dz = sy #size in z = y dimension
            dy = sy #size in y
            dz = boxWallT #size in y = wall thinckness

            if type == 'opening':
                if position[1] > 0:
                    holepos = (position[0]+fx, boxL-(boxWallT/2), position[2]+fy)
                else:
                    holepos = (position[0]+fx, -boxL+(boxWallT/2), position[2]+fy)
            elif type[0:4] == 'wire':
                rtyp = type.split('-')[1]
                if rtyp == 'roty':
                    bpy.ops.mesh.primitive_cylinder_add( radius=1, depth=10)
                    SNULLE

        elif ry == 90:
            rrx = 0
            rry = 90
            dx = sx
            dy = sy
            dz = boxWallT
            if type == 'opening':
                if position[0] > 0:
                    holepos = (boxW-(boxWallT/2), position[1]+fx, position[2]+fy)
                else:
                    holepos = (-boxW+(boxWallT/2), position[1]+fx, position[2]+fy)
            else:
                pass

        if holeshape == 'cube':
            hole_ob = CreateCube(holepos,dx/2, dy/2, dz, rrx, rry, rrz)
        elif holeshape == 'cylinder':
            #CreateCylinder(position, depth, sxhalf,syhalf,szhalf,rx,ry)
            holedepth = dx/2
            hole_ob = CreateCylinder(holepos, holedepth, dx/2, dy/2, dz, rrx, rry, rrz)
            #hole_ob = CreateCylinder(holepos, rimwidth+0.1, dx/2, dy/2, (rimheight/2+0.1), rx, ry)

            #SNULLE
            #hole_ob = CreateCylinder(holepos, dz, 3, 2, dz, rrx, rry)

        DiffObs(platform_ob, hole_ob)

## CPrint the output

if doPly:
    FPN = '%s.ply' % (FPNnoExt,)
    bpy.ops.export_mesh.ply(filepath=FPN)

'''
if doPStl:
    FPN = '%s.stl' % (FPNnoExt,)
    bpy.ops.export_mesh.ply(filepath=FPN)

if doObj:
    FPN = '%s.obj' % (FPNnoExt,)
    bpy.ops.export_mesh.ply(filepath=FPN)
'''

```

### xml

```
<?xml version='1.0' encoding='utf-8'?>
<dim>

	<output ply='1' stl='0' obj='0'>
			/Users/thomasgumbricht/docs-local/STL_models/2020/spectro-soild-sampler_20200328_v18b
	</output>

	<box W='29.7' L='15.6' H='5.7' wallT='2' roofT='2.0' floorT='2.0' cornerradius='0' innerrim='0' outerrim='0' rimheight='0'></box>

	<structures>

		<item id='samplearea' baseshape = 'cube' inside='1'  W='15' L='13.4' H='10' centerx='0' centery='0.4' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='6' embed='1'>
		</item>

		<item id='rim' baseshape = 'cube' inside='0'  W='30.6' L='0' H='1' centerx='0' centery='-7' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='9.1' embed='0'>
		</item>

		<item id='lip' baseshape = 'cube' inside='0'  W='36' L='0' H='1' centerx='0' centery='-9' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='12' embed='0'>
		</item>

		<item id='handle' baseshape = 'cube' inside='0'  W='6' L='0' H='1' centerx='0' centery='-14' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='12' rimheight='2' embed='0'>
		</item>

		<item id='text' baseshape = 'text' text='Stulturum;   2020' inside='0'  W = '4' L = '4' H = '1' centerx='-8' centery='-15' centerz='2' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='0' embed='1'>
		</item>

	</structures>

</dim>
```
