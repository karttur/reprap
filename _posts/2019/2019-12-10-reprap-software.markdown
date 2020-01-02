---
layout: post
title: Reprap software
categories: blog
excerpt: "Software for designing and printing 3D objects"
tags:
  - reprap
  - software
  - Blender
  - Meshmixer
  - repetier-host
  - German reprap PRotos V2
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-10 11:27'
modified: '2019-12-10 11:27'
comments: true
share: true
---

## Introduction

I use <span class='app'>Blender</span> for designing and drawing 3D models. To transfer the models from <span class='app'>Blender</span> to the printing app (<span class='app'>Repetier-host</span>) I have to go via <span class='app'>Meshmixer</span>. My processing chain for designing and printing 3D objects thus includes three apps.

## Blender

Different versions of [<span class='app'>Blender</span>](https://www.blender.org) have different bugs. To design and draw 3D objects I use [version 2.76 (05-Nov-2015)](https://download.blender.org/release/Blender2.76/). The download for Mac OSX is a disk image (<span class='file'>dmg</span>). The <span class='file'>dmg</span> file only contains the app, just drag it to the <span class='file'>Applications</span> folder. As there is no other installation required, once you have copied the app you can simply rename it (to Blender276.app in my example).

## Meshmixer

I use [<span class='app'>Meshmixer</span>](https://www.meshmixer.org) for converting my 3D models between different formats. But it can also be used for more advances processing.

## Repetier-Host

My [German RepRap PRotos V2](https://3dprintingindustry.com/news/german-repraps-upgraded-protos-v2-bigger-easier-build-19846/) uses [<span class='app'>Repetier</span>](https://www.repetier.com) and [<span class='app'>slic3r</span>](https://slic3r.org) for printing. It is enough to download and install <span class='app'>Repetier</span> as it includes <span class='app'>slic3r</span>.
