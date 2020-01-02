---
layout: post
title: Design a kayak rudder, part 1
categories: blog
excerpt: "Design a kayak rudder in Blender using lattice modifier"
tags:
  - reprap
  - Blender
  - lattice
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-12 11:27'
modified: '2019-12-12 11:27'
comments: true
share: true
---

## Introduction

Creating complex forms in <span class='app'>Blender</span> that involves twisting, dragging or otherwise distorting a basic shape is tricky to do using scripting. Instead you attach a lattice over your original form and then interactively massage individual, or grouped, nodes from the lattice and the original form will follow. In this tutorial I show how to create a rudder for a kayak starting from a cylinder.

## Start Blender with clean view

Start <span class='app'>Blender</span> (in my case Blender276.app - see [previous](../reprap-software/) post).

<figure>
<img src="../../images/blender-rudder01.png">
<figcaption> Initial GUI of Blender, object(s) in orange are active. </figcaption>
</figure>

For the first part of this manual the 3D viewer mode must be set to _Object mode_. Just below the 3D viewing area you should see the text _Object mode_ (illustrated in figure 2).

Sequentially remove the objects in the 3D view. Click on the object to remove (either in the 3D view or in the object frame at the top of the column to the right of the 3D view). The selected object turns orange. If you do not manage to select an object, you can use the _Select_ menu and its options towards the GUI bottom left (see figure 2).

<figure>
<img src="../../images/blender-rudder02.png">
<figcaption> Alternative select methods under the Select menu. </figcaption>
</figure>

With the object selected move the cursor to the 3d view (do not click the cursor, it just has to be _in_ the 3D view), click the _Delete_+_function_ (_<--_+_fn_) keys simultaneously, and a small confirmation box should pop up in the 3D view (see figure below).

<figure>
<img src="../../images/blender-rudder03.png">
<figcaption> To delete an object first select it then press fn+del keys at the same time with the cursor in the 3D view. </figcaption>
</figure>

## Add basic form

With a clean 3d view, change the left column to _Create_ from the vertical tabs along the very left margin. If you want the object to be exactly at the center, simultaneoulsy click _shift_+_S_ keys and select the option _Cursor to Center_.

<figure>
<img src="../../images/blender-rudder04.png">
<figcaption> Click _shift_+_S_ keys to position the cursor. </figcaption>
</figure>

Add the basic form you want to use to start with. In the example below I have added a cylinder. In the left column, below the list of basic shapes, the default parameters set for the shape you select appear: _Vertices_, _Radius_, _Depth_, _Cap Fill Type_, _Align to View_, _Location_ and _Rotation_. You can alter these parameters directly, or us the short keys and enter codes/numbers as described in the the next session.

<figure>
<img src="../../images/blender-rudder05.png">
<figcaption> Add the basic form you want to start with. </figcaption>
</figure>

## Position your basic shape

This step is not strictly necessary, you can always do it as a post-processing step. But I think it is easier to do it now. The things you need to consider is object position and size. Ideally you want to construct your 3D object so that it can be directly transferred to your 3D printer. This means that the bottom (of your future printed 3D item) should be where Z = 0. In my case I want to print the rudder in 2 halves, and I thus need to rotate the cylinder 90 degrees around either the x or the y axis. Make sure the cylinder is the selected object, press the _R_ key, followed by the _X_ key, then type _90_ and hit return. Alternatively just write _90_ for the parameter _Rotation_ -> _X_ in the left column.

<figure>
<img src="../../images/blender-rudder06.png">
<figcaption> Rotate the object by pressing the R key, followed by the axis around which you want to rotate and the degrees of the rotation movement. Or enter the rotation in the left column and the object will rotate interactively.</figcaption>
</figure>

Similarily, if you want to change the size, just press the _S_ key, and enter a size factor. This affects all axis equally. To set different size factors on different axis hit the corresponding axis key (X,Y,Z) before entering the scale factor. You can only change one axis at a time. As the rudder form will be elliptic, you can create a more elliptic shape by increasing _Y_ and _X_ and leave _Z_. In the example below I have set both _X_ and _Y_ to a factor of 3.

<figure>
<img src="../../images/blender-rudder07.png">
<figcaption> Resize the object by pressing the S key, followed by the axis around which you want to change the size and enter a size factor to apply.</figcaption>
</figure>

## Add and setup lattice

To add a new form, simultaneously press the _Shift_+_A_ keys, and then select the basic shape you desire (_lattice_ in this tutorial). With the lattice selected, change its size (press the _S_ key followed by the axis a factor and then return) to fit the original object. if you changed the size of the original object you have to make similar changes to the lattice size.

<figure>
<img src="../../images/blender-rudder08.png">
<figcaption> Add lattice through pressing the Shift+A keys and then resize by pressing the S key. The lattice should fit the oblect you want to transform. </figcaption>
</figure>

With the lattice still selected, click the _Object Data_ button (looks like a small window frame - the blue button in the figure below) in the object menu (in the right column). In the menu that then appears you can set the node density in X(U), Y(V) and Z(W). In the example below I have added 2 nodes to U (total = 4) and 1 node to V (total = 3) for illustration purposes. I suggest that you add so that you get 4 or 5 nodes per axis.

<figure>
<img src="../../images/blender-rudder09.png">
<figcaption> From the object menu select Object Data and set the number of nodes per axis of the lattice. </figcaption>
</figure>

## Attach lattice to original object

![blender-rudder10](../../images/blender-rudder10.png)
{: .pull-right}

Select the original object (cylinder in the example) and click the _Object modifier_ button (the small spanner - blue in the example to the right) in the object menu.

The right column will change appearance and only contain a drop down menu for selecting _Add Modifier_. Click and select _lattice_ from the overwhelming amount of alternatives, as shown below.

<figure>
<img src="../../images/blender-rudder11.png">
<figcaption> Add modifier lattice to the basic shape (cylinder). </figcaption>
</figure>

![blender-rudder12](../../images/blender-rudder12.png)
{: .pull-right}

The chosen modifier _type_ shows up as a window with options below the drop down menu. In that small window there is one item for _Object_ (showing a small orange cube and an eye-dropper). Click on the cube, and a drop down list appears showing your alternatives. It should only contain one item, namely your _Lattice_ as shown to the right. Select it.

## Lattice object modifier

To "activate" the attached lattice for transforming the underlying object (cylinder), you have to do two things: first select the lattice as the active object and then change the 3D view mode to _Edit mode_. Illustrated in the figure below. The lattice will now show up as a a swarm of nodes.

<figure>
<img src="../../images/blender-rudder13.png">
<figcaption> Activate the lattice transformation mode by selecting the lattice as the active object and change the 3D-view mode to Edit mode. </figcaption>
</figure>

![blender-rudder13](../../images/blender-rudder13.png)
{: .pull-right}

To actually use the lattice for transforming your object, you have to select one or more of the nodes, and then whatever you choose to do, will affect the selected nodes. Use the _Select_ menu to define how to select nodes, I prefer using the _Border Select_ option (also reached by just pressing the _B_ key). When selecting a new set of nodes, you first have to _(De)Select All_ (or press the _A_ key).

Selected nodes turn orange, and at the same time the transformation tool will show up. The default setting of the transformation tool is _Translate_, indicated by arrowheads (illustrated in the image in the next section). Other alternatives are _Rotate_ and _Scale_ (explained further down).

## Transform along axis

The form I want to create is a typical rodder shape - a bit thicker towards the bow (where it is attached to the hull) and getting thinner towards the stern. As I have placed my cylinder that means I need to drag my object to become thinner along the x-axis. I thus select all nodes on either side of the y-axis and then _Translate_ the lattice by pulling the selected nodes with the xaxis arrow. The underlying form follows along.

<figure>
<img src="../../images/blender-rudder14.png">
<figcaption> Translate x-axis by pulling it out to a basic rudder shape. </figcaption>
</figure>

## Scale

When pulling out (_Translate_) the rudder towards the stern, the proportions between length and height become skewed. To fix that you need to _Scale_ the object along the axis where it is too short.

![blender-rudder15](../../images/blender-rudder15.png)
{: .pull-left}
To increase the height select all the nodes in the lattice. Change from the _Translate_ tool (with arrowheads) to the _Scale tool_ (with cube heads) as illustrated to the left.

As I have placed my rudder (for 3D printing reasons), the height is along the x-axis. The figure below illustrates the _Scale_ function applied along the x-axis.

<figure>
<img src="../../images/blender-rudder16.png">
<figcaption> Scale x-axis by the scale tool. </figcaption>
</figure>

## Rotate

The _Rotate tool_ rotates the selected nodes vis-á-vis each other. It is a bit tricky to use.

<figure>
<img src="../../images/blender-rudder17.png">
<figcaption> Rotate tool. </figcaption>
</figure>

## Finish and export

With the lattice modifier you can get quite far towards creating a kayak rudder. There are other tools you can use, but I will accept the result shown below. Select the rudder (cylinder) as the active object and then export it as an <span class='file'>.obj</span> file as shown below. In the next post I will show how to import the rudder to <span class='app'>Blender</span> and cut it, all using Python scripting

<figure>
<img src="../../images/blender-rudder18.png">
<figcaption> Export the rudder as an obj file. </figcaption>
</figure>
