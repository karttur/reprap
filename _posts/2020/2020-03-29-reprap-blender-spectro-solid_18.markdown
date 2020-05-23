---
layout: post
title: Design spectrometer v 18
categories: spectromodel
excerpt: "Design spectrometer."
tags:
  - reprap
  - Blender
  - python
  - advent
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2020-03-29 11:27'
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

imprint = 'v0.18 \nMar 2020'
imprint = False
xmlFN = 'Users/thomasgumbricht/docs-local/blender-py-params/spectro-solid_20200328_v18.xml'

xmlFN = 'Users/thomasgumbricht/docs-local/blender-py-params/spectro-solid-holder_20200329_v18.xml'

#FP = "/Users/thomasgumbricht/docs-local/STL_models/2020/spectro-soild_20200328_v18a.ply"

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
            pz = 0
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

def CreateText(position, rotation, textstr, depth=1, font='arial', fontsize=16):
	#create the text object
    #bpy.ops.object.text_add( location=(-29, -15, 3 ) )
    bpy.ops.object.text_add( location=(-6, -8, 2 ) )
    mytext = bpy.data.objects["Text"]
    mytext.data.body = imprint
    #mytext.data.body = 'Stulturum\nv0.017d\nMar 2020'
    #set some stuff up
    #mytext.data.align_x = "CENTER"
    #mytext.data.align_y = "BOTTOM"
    mytext.data.extrude = 0.2
    #fnt = bpy.data.fonts.load(font_loc)              #font loading works
    #mytext.data.font = fnt
    bpy.context.scene.objects.active = mytext   # make sure my Text object is correctly selected
    mytext.select = True
    bpy.ops.object.convert(target="MESH") # Convert to mesh

    #SizeRotateItem(6, 6, 6, 0, 0, 90)
    SizeRotateItem(6, 6, 6, 0, 0, 0)

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

### link to xml
#xmlFN = '/Volumes/ECLIPSE/spectrodim_2020_v01.xml'
#xmlFN = 'Users/thomasgumbricht/docs-local/blender-py-params/spectrodim_20200319_v17.xml'
#xmlFN = 'Users/thomasgumbricht/docs-local/blender-py-params/spectrodim_20200130_v15.xml'

### Parse xml file
dom = minidom.parse(xmlFN)

### Box paramters
boxTag = dom.getElementsByTagName('box')
boxW = float(boxTag[0].getAttribute('W'))/2
boxL = float(boxTag[0].getAttribute('L'))/2
boxWallT = float(boxTag[0].getAttribute('floorT'))
boxCornerR = float(boxTag[0].getAttribute('cornerradius'))

### lock parameters

if lock:
    floorTag = dom.getElementsByTagName('top')
    boxH = float(floorTag[0].getAttribute('H'))
    boxFloorT = float(floorTag[0].getAttribute('T'))
    floorOuterRim = float(floorTag[0].getAttribute('outerrim'))
    floorInnerRim = float(floorTag[0].getAttribute('innerrim'))
    rimHeight = float(floorTag[0].getAttribute('rimheight'))
else:
    floorTag = dom.getElementsByTagName('bottom')
    boxH = float(floorTag[0].getAttribute('H'))
    boxFloorT = float(floorTag[0].getAttribute('T'))
    floorOuterRim = float(floorTag[0].getAttribute('outerrim'))
    floorInnerRim = float(floorTag[0].getAttribute('innerrim'))
    rimHeight = float(floorTag[0].getAttribute('rimheight'))

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

#bpy.ops.object.duplicate_move()
#bottomplate_ob = bpy.context.object

bpy.ops.object.duplicate_move()
innerwall_ob = bpy.context.object

#scale the outerwall object

zfac = boxH/boxFloorT

# select and scale the outerwall
xfac = yfac = 1
ScaleMoveVertically(platform_ob, xfac, yfac, zfac, boxH/2-boxFloorT/2)

# select and scale the innerwall
xfac = (boxW-boxWallT)/boxW
yfac = (boxL-boxWallT)/boxL

ScaleMoveVertically(innerwall_ob, xfac, yfac, zfac, boxFloorT/2+(boxH/2))

## Take the diff from outerwall and innewall to get the wall
DiffObs(platform_ob,innerwall_ob)

##### Box outline ready

##### Do the imprint
if imprint:
    #del_ob = CreateText((-28,-15,3), (0,0,90), 'Stulturum')  
    del_ob = CreateText((0,0,2), (0,0,0), 'Stulturum')  

DiffObs(platform_ob,del_ob)

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
            #position = (0,0,0)       
            del_ob = CreateCylinder(position, 1, sx/2,sy/2,sz/2,rx,ry)
        elif baseshape == 'text':
        	text = item.getAttribute('text')
        	del_ob = CreateText(position, rotation, text)

            #del_ob = CreateCylinder(position,sx/2,sy/2,sz/2,rx,ry)
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

## Clean the transition between the wall and the rim


bpy.ops.export_mesh.ply(filepath=FP)

FP = "/Users/thomasgumbricht/docs-local/STL_models/2020/spectrobox_20200319_v17.stl"
#bpy.ops.export_mesh.stl(filepath=FP)

FP = "/Users/thomasgumbricht/docs-local/STL_models/2020/spectrobox-sampler_20200319_v17.obj"
#bpy.ops.export_mesh.obj(filepath=FP)

```

### xml

```
<?xml version='1.0' encoding='utf-8'?>
<dim>
	<box W='54.0' L='52.0' wallT='2.0' roofT='2.0' floorT='2.0' cornerradius='2'></box>

	<top H='16' T='3.0' innerrim='1.75' outerrim='0' rimheight='1.75' ></top>

	<bottom H='16' T='3.0' innerrim='1.75' outerrim='0' rimheight='1.75'></bottom>

	<structures>
		<!--
			The rotation needs to be fitted to the position as follows:
			Floor or roof: 0,0,0
			along front or back: 0,y,0
			along sides: x,0,0

			If embed is set, the breakout board will be forced to fit the inner wall floor or roof,
				regardless if that is correctly given or not. The rotation determins which side to use

			All positions are adjusted to fit inside the box, if that does not work out you have to enlarge the box
		-->

		<item id='spectrometer' baseshape = 'cube' inside='1'  W='26' L='28.5' H='2.5' centerx='0' centery='10' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='0' embed='0'>
			<hole id = 'spectrosensor' type = 'opening' holeshape = 'cube' W='6' L='6' fromcenterx='0' fromcentery='0' rotationx='0' rotationy='0'>
			</hole>
			<hole id = 'spectrolight' type = 'opening' holeshape = 'cube' W='3' L='3' fromcenterx='0' fromcentery='-5.5' rotationx='0' rotationy='0'>
			</hole>
			<hole id = 'spectroled' type = 'opening' holeshape = 'cube' W='3' L='3' fromcenterx='0' fromcentery='11.5' rotationx='0' rotationy='0'>
			</hole>
		</item>

		<item id='support1' baseshape = 'cube' inside='1'  W='0' L='10' H='12' centerx='-27' centery='-5' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='13' embed='0'>
		</item>

		<item id='support2' baseshape = 'cube' inside='1'  W='0' L='10' H='12' centerx='27' centery='-5' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='13' embed='0'>
		</item>

		<item id='support3' baseshape = 'cube' inside='1'  W='4' L='0' H='12' centerx='-14' centery='26' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='13' embed='0'>
		</item>

		<item id='support4' baseshape = 'cube' inside='1'  W='4' L='0' H='12' centerx='14' centery='26' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='13' embed='0'>
		</item>

		<item id='laser-levee' baseshape = 'cube' inside='1'  W='8' L='8' H='12' centerx='-19' centery='10' centerz='0' rotationx='0' rotationy='0' rotationz='31' rimwidth='2' rimheight='13' embed='0'>
		</item>

		<item id='rgb-levee' baseshape = 'cube' inside='1'  W='8' L='8' H='12' centerx='18' centery='10' centerz='0' rotationx='0' rotationy='0' rotationz='-33' rimwidth='2' rimheight='13' embed='0'>
		</item>

		<item id='laser-levee-opening' baseshape = 'cube' inside='1'  W='6' L='10' H='12' centerx='-17' centery='6.5' centerz='0' rotationx='0' rotationy='0' rotationz='31' rimwidth='0' rimheight='13.1' embed='0'>
		</item>

		<item id='rgb-levee-opening' baseshape = 'cube' inside='1'  W='6' L='10' H='12' centerx='16' centery='6.5' centerz='0' rotationx='0' rotationy='0' rotationz='-33' rimwidth='0' rimheight='13.1' embed='0'>
		</item>

		<item id='sensor-levee' baseshape = 'cube' inside='1'  W='8' L='12' H='12' centerx='0' centery='7' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='13' embed='0'>
		</item>

		<item id='sensor-levee-opening' baseshape = 'cube' inside='1'  W='6' L='13' H='12'  centerx='-0.1' centery='-2' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='13.1' embed='-0.1'>
		</item>

		<item id='laser' baseshape = 'cylinder' inside='1'  W = '4' L = '4' H = '30' centerx='-19' centery='10' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='0' embed='0'>
			<hole id = 'laserhole' type = 'opening' holeshape = 'cylinder' W='6.6' L='6.6'  fromcenterx='0' fromcentery='0' rotationx='0' rotationy='0'>
			</hole>
		</item>

		<item id='led' baseshape = 'cube' inside='1'  W = '9' L = '9' H = '4' centerx='18' centery='10' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='0' embed='0'>
			<hole id = 'light' W='8.3' L='8.3' type = 'opening' holeshape = 'cylinder' fromcenterx='0' fromcentery='0' rotationx='0' rotationy='15'>
			</hole>
		</item>

		<item id='magnet' baseshape = 'cylinder' inside='0'  W = '5.8' L = '5.8' H = '15' centerx='-12' centery='-6' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='0' embed='1'>
		</item>

		<item id='sampleholder' baseshape = 'cube' inside='1'  W='30.4' L='6.4' H='8' centerx='0' centery='-20' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='2' rimheight='13' embed='1'>
		</item>

		<item id='sampleholder_remover' baseshape = 'cube' inside='1'  W='24' L='6' H='10' centerx='0' centery='-15' centerz='0' rotationx='0' rotationy='0' rotationz='0' rimwidth='0' rimheight='13.1' embed='-0.1'>
		</item>

	</structures>

</dim>

```
