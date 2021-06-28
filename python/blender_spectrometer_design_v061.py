'''
Python script for running inside Blender

Created on 30 Jan 2021
last update 6 june 2021

Version: 0.61

@author: thomasgumbricht
'''

# runmode = True: For blander; runmode = False for eclipse testing
runmode = True

##### Imports
if runmode:
    import bpy
    import mathutils
import sys
from math import radians,sin,asin,cos,atan,tan,sqrt
from xml.dom import minidom

#####

# container
xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-box-AMS_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-lock_20210606_v061d.xml'


# direct sampler
xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-direct-cyl-led_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-direct-cyl-xenon_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-direct-cyl-red-laser_20210606_v061d.xml'

# Grind sampler
xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-solid-cyl-led_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-solid-cyl-xenon_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-solid-cyl-red-laser_20210606_v061d.xml'

# Cuvette

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-cuvette-trx_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-cuvette-front_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-cuvette-back-led_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-cuvette-xenon_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-cuvette-blue-led_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-cuvette-green-laser_20210606_v061d.xml'

xmlFN = '/Users/thomasgumbricht/docs-local/blender-py-params/v061/spectro-cuvette-red-laser_20210606_v061d.xml'

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
    '''Rotation and position adjustment
    '''
    if not runmode:
            print ('        FixRotations')
    if rx == ry == 0: # horizontal object, adjust z for embedding

        if not runmode:

            print ('        rx == ry == 0')
            print ('        location (input)', px,py,pz)
        dx = sx
        dy = sy
        dz = sz


        if pz == 0 and inside: #adjust z position to account for embedding
            pz = boxFloorT+sz/2-embed
            if not runmode:
                print ('altering pz from 0 to', pz)

    elif rx == 90: # Rotated around the x axis

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

    elif ry == 90: # Rotated around the y axis

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
        # Rotation, but not 90 degrees = ignore until later
        #    This is just a quick and dirty solution
        dx = sx
        dy = sy
        dz = sz
        if pz == 0 and inside:
            pz = boxFloorT+sz/2-embed

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
    #bpy.ops.mesh.primitive_cube_add( radius=2, location=(0,0,2), rotation=(0,0,0) )
    #ry = 15
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

    return SizeRotateItem(sxhalf,syhalf,szhalf,rx,ry,rz)

def CreateCone(position, depth, r1, r2, sxhalf, syhalf, szhalf, rx, ry, rz=0):

    bpy.ops.mesh.primitive_cone_add( radius1=r1, radius2=r2, depth=depth, location=position, rotation=(0,0,0) )

    return SizeRotateItem(sxhalf,syhalf,szhalf,rx,ry,rz)

def CreateSphere(position, sx, sy, sz, rx, ry, rz=0):

    bpy.ops.mesh.primitive_uv_sphere_add( location=position)

    return SizeRotateItem(sx,sy,sz,rx,ry,rz)


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

def PlatformCube():
    if not runmode:
        print ('PlatformCube')
        print ('    location', platformBoxPos)
        print ('    rotation',rotation)
    else:
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
        if boxCornerR:
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

        return platform_ob

def PlatformCylinder():
    if not runmode:
        print ('PlatformCylinder')
        print ('    location', platformBoxPos)
        print ('    rotation',rotation)
    else:
        ### create the first platform square and resize it
        bpy.ops.mesh.primitive_cylinder_add( radius=1, location=platformBoxPos, rotation=rotation)
        platform_ob = bpy.context.object
        ## Resize the platform
        bpy.ops.transform.resize(value=(boxW-boxCornerR, boxL, boxFloorT/2))

        return platform_ob

##### Initial parameters and defintions

### defualt rotation
rotation = (0,0,0)

if runmode:

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
boxshape = boxTag[0].getAttribute('baseshape')
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

if boxshape == 'cube':
    platform_ob = PlatformCube()
elif boxshape == 'cylinder':
    platform_ob = PlatformCylinder()
else:
    SnulleBulle


##### Platform ready

##### Make copies of the platform, for the outher and inner walls and the outer and innter rimes

xfac = yfac = 1

if runmode:
    # Copy the platform - the only object so far
    bpy.ops.object.select_all(action='SELECT')

    # Craete the inner room
    bpy.ops.object.duplicate_move()

    innerwall_ob = bpy.context.object

    ##### Create rim if requested

    if ( boxInnerRim or boxOuterRim ) and boxRimHeight:
        # Set z-fac for rim
        zfac = boxRimHeight/boxFloorT

        if boxOuterRim: # This creates an outer rime

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

        else: # This creates an inner rime

            bpy.ops.object.duplicate_move()

            rim_ob = bpy.context.object

            # select and scale the outerwall
            ScaleMoveVertically(rim_ob, xfac, yfac, zfac, boxH-1.45*boxRimHeight)

            # Create the eraser object

            bpy.ops.object.duplicate_move()

            rimdel_ob = bpy.context.object

            negative_rim = boxWallT-boxInnerRim

            xfac = yfac = (boxW - negative_rim)/boxW

            ScaleMoveVertically(rimdel_ob, xfac, yfac, 2, 0)

            DiffObs(rim_ob, rimdel_ob)

else:
    if ( boxInnerRim or boxOuterRim ) and boxRimHeight:
        # Set z-fac for rim
        zfac = boxRimHeight/boxFloorT

        if boxOuterRim: # This creates an outer rime
            print ('boxOuterRim')
            print ('    xfac, yfac, zfac', xfac, yfac, zfac)
            print ('boxInnerRim - eraser')
            xfac = yfac = (boxW-boxOuterRim)/boxW
            print ('    xfac, yfac, zfac', xfac, yfac, zfac)
        else:
            print ('boxInnerRim')
            print ('    xfac, yfac, zfac', xfac, yfac, zfac)
            print ('boxOuterRim - eraser')
            xfac = yfac = (boxW - negative_rim)/boxW
            print ('    xfac, yfac, zfac', xfac, yfac, zfac)

# reset xfac and yfac, set the z scale factor
xfac = yfac = 1
zfac = boxH/boxFloorT

if runmode:

    # select and scale the outerwall

    ScaleMoveVertically(platform_ob, xfac, yfac, zfac, boxH/2-boxFloorT/2)

else:
    print ('Outerwall')
    print ('    xfac, yfac, zfac', xfac, yfac, zfac)

# select and scale the innerwall
xfac = (boxW-boxWallT)/boxW
yfac = (boxL-boxWallT)/boxL

if runmode:
    ScaleMoveVertically(innerwall_ob, xfac, yfac, zfac, boxFloorT/2+(boxH/2))

    ## Take the diff from outerwall and innewall to get the wall
    DiffObs(platform_ob,innerwall_ob)

    ##### Box outline ready

    if boxOuterRim and boxRimHeight:
        UnionObs(platform_ob,rim_ob)

    if boxInnerRim and boxRimHeight:
        DiffObs(platform_ob,rim_ob)

else:
    print ('Innerwall')
    print ('    xfac, yfac, zfac', xfac, yfac, zfac)

##### Get all the breakout boards

structTag = dom.getElementsByTagName('structures')
## Get the square breakout boards
items = structTag[0].getElementsByTagName("item")

for item in items:

    itemid = item.getAttribute('id')
    baseshape = item.getAttribute('baseshape')
    inside = int(item.getAttribute('inside'))
    embed = float(item.getAttribute('embed'))
    if item.hasAttribute("removeonly"):
        removeonly = int(item.getAttribute('removeonly'))
    else:
        removeonly = 0
    if item.hasAttribute("removerim"):
        removerim = int(item.getAttribute('removerim'))
    else:
        removerime = 0


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


    if not runmode:
        print ('item',itemid)
        print ('    shape',baseshape)
        print ('    inside, embed',inside,embed)
        print ('    WxLxH',sx,sy,sz)
        print ('    location', px,py,pz)
        print ('    rotation',rx,ry,rz)
        print ('    rimWxH', rimwidth, rimheight)

    ### Fix the rotation, only rotations in x and y are valid, rotation in z is simply changing W and L

    dx,dy,dz,px,py,pz = FixRotations(px,py,pz,sx,sy,sz,rx,ry,rz,inside)
    if not runmode:
        print ('    location (adjusted)', px,py,pz)
        print ('    WxLxH (adjusted)', dx,dy,dz)

    ### Set the position
    position = (px,py,pz)

    if baseshape == 'sphere':

        sob = CreateSphere(position, sx, sy, sz, rx, ry, rz=0)

        UnionObs(platform_ob, sob)

    if embed: #if the wall, roof or floor is going to be carved out to fir the item
        if runmode:
            ## create the platform square and rescale it
            if baseshape == 'cube':
                del_ob = CreateCube(position, sx/2,sy/2,sz/2,rx,ry)
            elif baseshape == 'cylinder':
                del_ob = CreateCylinder(position, 1, sx/2,sy/2,sz/2,rx,ry)
            elif baseshape == 'text':
                text = item.getAttribute('text')
                textT = text.split(';')
                newText = textT[0]
                for t in range(1,len(textT)):
                    newText = '%s\n%s' % (newText, textT[t])

                storlek = (sx, sy, sz)
                rotate = (rx,ry,rz)
                del_ob = CreateText(storlek, position, rotate, newText)
            elif baseshape== 'cone':
                D1 = float(item.getAttribute('D1'))
                D2 = float(item.getAttribute('D2'))
                R1 = D1/2
                R2 = D2/2
                del_ob = CreateCone(position, sz, R1, R2, sx,sy,1, rx, ry)

            else:
                print ('Undefined shape in time embed')
                SNULLE

            #Cut out the material for the item site inside the box

            DiffObs(platform_ob,del_ob)
        else:
            if baseshape == 'cube':
                print ('Deleting embedded cube',position,1, sx/2,sy/2,sz/2,rx,ry)
            elif baseshape == 'cylinder':
                print ('Deleting embedded cylinder',position, 1, sx/2,sy/2,sz/2,rx,ry)


    if rimwidth or rimheight:

        if inside:
            if rx == ry == 0: # horizontal object, adjust z for embedding
                position = (px,py,boxFloorT+rimheight/2)
                if not runmode:
                    print ('    building inside floor rim')
                    print ('        position',position)

            elif rx == 90: # Rotated around the x axis

                position = (px,py,pz)
                if not runmode:
                    print ('    building inside Y-wall rim')
                    print ('        position',position)

                '''
                if py < 0:
                    position = (px,py+rimheight/2,pz)
                    if not runmode:
                        print ('    building inside Y-wall rim')
                        print ('        position',position)
                else:
                    position = (px,py-rimheight/2,pz)
                    if not runmode:
                        print ('    building inside Y-wall rim')
                        print ('        position',position)
                '''

            elif ry == 90: # Rotated around the x axis

                position = (px,py,pz)
                if not runmode:
                    print ('    building inside X-wall rim')
                    print ('        position',position)

                '''
                if px < 0:
                    position = (px+rimheight/2,py,pz)
                    if not runmode:
                        print ('    building inside X-wall rim')
                        print ('        position',position)
                else:
                    position = (px-rimheight/2,py,pz)
                    if not runmode:
                        print ('    building inside X-wall rim')
                        print ('        position',position)
                '''

        else:
            if rx == ry == 0: # horizontal object, adjust z
                position = (px,py,pz+rimheight/2)
                if not runmode:
                    print ('    building outside floor rim')
                    print ('        position',position)

            elif rx == 90: # Rotated around the x axis

                position = (px,py,pz)
                if not runmode:
                    print ('    building outside Y-wall rim')
                    print ('        position',position)

                '''
                if py < 0:

                    position = (px,py-rimheight/2,pz)
                    if not runmode:
                        print ('    building outside Y-wall rim')
                        print ('        position',position)
                else:
                    position = (px,py+rimheight/2,pz)
                    if not runmode:
                        print ('    building outside Y-wall rim')
                        print ('        position',position)
                '''

            elif ry == 90: # Rotated around the x axis

                position = (px-rimheight/2,py,pz)
                if not runmode:
                    print ('    building outside X-wall rim')
                    print ('        position',position)

                '''
                if px < 0:
                    position = (px-rimheight/2,py,pz)
                    if not runmode:
                        print ('    building outside X-wall rim')
                        print ('        position',position)
                else:
                    position = (px+rimheight/2,py,pz)
                    if not runmode:
                        print ('    building outside X-wall rim')
                        print ('        position',position)
                '''

        ## Create frame

        if baseshape == 'cube':
            if not rimwidth:
                if runmode:
                    del_ob = CreateCube(position,sx/2,sy/2,rimheight/2,rx,ry, rz)

                    DiffObs(platform_ob, del_ob)
                else:
                    print ('    deleting cube')
                    print ('        position',position)
                    print ('        size',sx/2,sy/2,rimheight/2)
                    print ('        rotation',rx,ry, rz)

            # Create outer frame
            if sx * sy != 0: #width or length
                if runmode and not removeonly:
                    frame_ob = CreateCube(position,sx/2+rimwidth, sy/2+rimwidth, rimheight/2, rx, ry, rz)

                else:
                    print ('    building outer cube')
                    print ('        position',position)
                    print ('        size',sx/2,sy/2,rimheight/2)
                    print ('        rotation', rx, ry, rz)
            else:
                if runmode and not removeonly:
                    frame_ob = CreateCube(position,sx/2+rimwidth/2, sy/2+rimwidth/2, rimheight/2, rx, ry, rz)
                else:
                    print ('    building outer cube')
                    print ('        position',position)
                    print ('        size',sx/2,sy/2,rimheight/2)
                    print ('        rotation', rx, ry, rz)
            # Create inner frame
            if sx * sy != 0:
                if runmode:
                    del_ob = CreateCube(position,sx/2,sy/2,1.01*rimheight/2,rx,ry, rz)
                else:
                    print ('    building inner remove cube')
                    print ('        position',position)
                    print ('        size',sx/2,sy/2,1.01*rimheight/2)
                    print ('        rotation', rx, ry, rz)

        elif baseshape == 'cylinder':
            depth = 2

            if sx * sy != 0: #width or length
                if runmode and not removeonly:
                    frame_ob = CreateCylinder(position, depth, sx/2+rimwidth, sy/2+rimwidth, rimheight/2, rx, ry)

                else:
                    print ('    building outer cyliner')
                    print ('        depth, position',depth, position)
                    print ('        size',sx/2,sy/2,rimheight/2)
                    print ('        rotation',rx,ry, rz)
            else:
                if runmode and not removeonly:
                    frame_ob = CreateCylinder(position, depth, sx/2+rimwidth/2, sy/2+rimwidth/2, rimheight/2, rx, ry)
                else:
                    print ('    building outer cylinder')
                    print ('        position',position)
                    print ('        size',sx/2,sy/2,rimheight/2)
                    print ('        rotation', rx, ry, rz)
            # Create inner frame
            if sx * sy != 0:
                if runmode:
                    del_ob = CreateCylinder(position,2,sx/2,sy/2,1.01*rimheight/2,rx,ry)
                else:
                    print ('    building inner remove cylinder')
                    print ('        position',position)
                    print ('        size',sx/2,sy/2,1.01*rimheight/2)
                    print ('        rotation', rx, ry, rz)


        elif baseshape == 'cone':
            D1 = float(item.getAttribute('D1'))
            D2 = float(item.getAttribute('D2'))
            R1 = D1/2
            R2 = D2/2

            # Reset position
            if rx == ry == 0:
                position = (position[0], position[1], rimheight/2)
                if not runmode:
                    print ('    Cone position reset',position)
            elif rx == 90:
                NOTYET
            elif ry == 90:
                NOTYET
            else:
                position = (position[0], position[1], rimheight/2)
                if not runmode:
                    print ('    Cone position reset',position)
            # Create outer frame

            if sx * sy != 0: #width or length
                if runmode and not removeonly:

                    frame_ob = CreateCone(position, rimheight, R1+rimwidth, R2+rimwidth, sx,sy,1, rx, ry)

                else:

                    print ('    building outer cone')
                    print ('        R1,R2, position',R1+rimwidth,R2+rimwidth, position)
                    print ('        size',sx/2,sy/2,rimheight)
                    print ('        rotation',rx,ry, rz)
            else:
                if runmode:
                    frame_ob = CreateCone(position, rimheight, sx/2+rimwidth, sy/2+rimwidth, 1,1,1, rx, ry)

                else:
                    print ('    building outer cone')
                    print ('        R1,R2, position',R1,R2, position)
                    print ('        size',sx/2,sy/2,rimheight)
                    print ('        rotation', rx, ry, rz)
            # Create inner frame
            if sx * sy != 0:
                if runmode:

                    del_ob = CreateCone(position, rimheight, R1, R2, sx,sy,1.01, rx, ry)
                else:
                    print ('    building inner remove cone')
                    print ('        R1,R2, position',R1,R2, position)
                    print ('        size',sx/2,sy/2,1.01*rimheight)
                    print ('        rotation', rx, ry, rz)

        ## Create the frame by taken difference between frame_ob and del_ob

        if runmode:
            if removeonly:
                DiffObs(platform_ob, del_ob)
            else:
                if sx * sy != 0:
                    DiffObs(frame_ob, del_ob)

                if rx not in [0,90] or ry not in [0,90]:
                    #Remove excess stuff
                    ### create a below z=0 cube and remove any excess stuff
                    bpy.ops.mesh.primitive_cube_add( radius=1, location=(position[0], position[1],-5), rotation=(0,0,0))
                    undersida_ob = bpy.context.object
                    ## Resize the platform
                    if baseshape == 'cone':
                        smx = max(D1, D2)
                    else:
                        smx = max(sx, sy)
                    bpy.ops.transform.resize(value=(smx, smx, 6))

                    DiffObs(frame_ob, undersida_ob)

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
        if hole.hasAttribute("rotationz"):
            hrz= int(item.getAttribute('rotationz'))
        else:
            hrz = 0


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

                    holepos = (position[0]+fx, position[1]+fy, position[2]+0.5)


        elif rx == 90:
            rrx = 90
            rry = 0
            dx = sx #size in x

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

        else:
            rrx = hrx
            rry = hry
            rrz = hrz
            dx = sx
            dy = sy
        if runmode:
            if holeshape == 'cube':

                hole_ob = CreateCube(holepos,dx/2, dy/2, dz, rrx, rry, rrz)

            elif holeshape == 'cylinder':

                holedepth = dx/2

                hole_ob = CreateCylinder(holepos, holedepth, dx/2, dy/2, dz, rrx, rry, rrz)

            DiffObs(platform_ob, hole_ob)
        else:

            print ('        create hole')
            print ('            holepos',holepos)
            print ('            size',dx/2, dy/2, dz)
            print ('            rotation', rrx, rry, rrz)

## CPrint the output
if runmode:
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
