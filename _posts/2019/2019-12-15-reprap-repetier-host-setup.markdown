---
layout: post
title: Configure Repetier-Host
categories: blog
excerpt: "Configure Repetier-Host Mac for printing with the German RepRap PRotos V2"
tags:
  - reprap
  - software
  - Repetier
  - repetier-host
  - German RepRap Protos V2
  - configuration
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-15 11:27'
modified: '2019-12-15 11:27'
comments: true
share: true
---

## Introduction

This post goes through the configurations required for connecting the [German RepRap PRotos V2](https://www.3ders.org/articles/20130722-german-reprap-launches-protos-v2-3d-printer.html) to the software [Repetier](https://www.repetier.com) on Mac OSX. The instructions follows the [Repetier-Host Mac Documentation](https://www.repetier.com/documentation/repetier-host-mac/installation-and-connection/).

## Repetier-Host

Download and install [<span class='app'>Repetier-Host</span>](https://www.repetier.com/download-software/) as described in the [previous post](../reprap-software/).

Start <span class='app'>Repetier-Host</span>. Get to _Printer Settings_ via the menu:

<span class='menu'>Printer -> Printer Settings</span>

or hit the [cmp]+[p] keys at the same time.

### Printer Settings

In the Printer settings window, add a name of the configuration you want to create. You will need one configuration per printer per printing material. Thus, if you want to use different materials, you should set the name to reflect the material. In the example below I have called my configuration "PROTOS-V2-PLA".

#### Connection

if the _Connection_ is not correctly set, you will not be able to communicate with your printer. You have to give the _Port_, and probably the _Baud Rate_ will differ comapred to the default. You need to check the documentation of your 3D-printer to get the correct _Baud Rate_. The other parameters will most likely work by leaving the defaults.

<figure>
<img src="../../images/repetier-printer-config-connection.png">
<figcaption> Repetier-Host connection configuration for German RepRap PRotos V2.</figcaption>
</figure>

#### Behaviour

Under the <span class='tab'>Behaviour</span> tab, you need to change the _Default Extruder Temperature_ and the _Default heated bed temperature_  to fit your printer, its heated bed and the material. The _Travel Feedrate_ depends on the extruder opening. The German RepRap PRotos V2 can travel at higher speed then the default. The smaller extruder (1.75 mm) can travel as fast as 10800 mm/min and the larger (3 mm) at 6000 mm/min.

<figure>
<img src="../../images/repetier-printer-config-behaviour.png">
<figcaption> Repetier-Host behaviour configuration for German RepRap PRotos V2, PLA material.</figcaption>
</figure>

#### Dimension

The German RepRap PRotos V2 is a bit larger (230 mm) compared to the default (200 mm) settings of <span class='app'>Repetier-Host</span>.

<figure>
<img src="../../images/repetier-printer-config-dimension.png">
<figcaption> Repetier-Host behaviour configuration for German RepRap PRotos V2, PLA material.</figcaption>
</figure>

#### Advanced

The advances settings can safely be left blanc.

<figure>
<img src="../../images/repetier-printer-config-advanced.png">
<figcaption> Repetier-Host behaviour configuration for German RepRap PRotos V2, PLA material.</figcaption>
</figure>

#### Done

You should now be able to connect to your 3D-printer using <span class='app'>Repetier-Host</span>.
