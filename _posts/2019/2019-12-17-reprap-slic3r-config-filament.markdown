---
layout: post
title: Slic3r Filament settings
categories: blog
excerpt: "Configure filament setting in Slic3r"
tags:
  - reprap
  - Slic3r
  - configuration
  - filament setting
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2019-12-17 11:27'
modified: '2019-12-17 11:27'
comments: true
share: true
---

## Introduction

For each filament material and diameter, as well as nozzle diameter, you have to define different parameter for __print settings__ ([previous post](../reprap-slic3r-config-print)), __filament settings__ (this post) and/or __printing settings__ ([next page(../reprap-slic3r-config-printing)]).

## Prerequisits

<span class='app'>Slic3r</span> is installed with <span class='app'>Repetier-host</span>.

### Print settings

You get to the <span class='app'>Slic3r</span> page for print setting from the menu:

<span class='menu'>Settings -> Print Settings... </span>

The __filament settings__ is defined in 5 different pages.

- Filament
- Cooling
- Custom G-code
- Notes
- Overrides

But you only need to set the parameters of the first (_Filament_) page.

<figure>
<img src="../../images/slic2r-filament-settings-01.png">
<figcaption> Slic3r Filament Settings, Filament.</figcaption>
</figure>

<figure>
<img src="../../images/slic2r-filament-settings-02.png">
<figcaption> Slic3r Filament Settings, Cooling.</figcaption>
</figure>

<figure>
<img src="../../images/slic2r-filament-settings-03.png">
<figcaption> Slic3r Filament Settings, Custom G-codes.</figcaption>
</figure>

<figure>
<img src="../../images/slic2r-filament-settings-04.png">
<figcaption> Slic3r Filament Settings, Notes.</figcaption>
</figure>

<figure>
<img src="../../images/slic2r-filament-settings-05.png">
<figcaption> Slic3r Filament Settings, Overrides.</figcaption>
</figure>
