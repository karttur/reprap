---
layout: post
title: Design spectrometer v 061d
categories: spectromodel
excerpt: "Design spectrometer."
tags:
  - reprap
  - Blender
  - python
  - spectrometer
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2021-06-06 11:27'
modified: '2021-06-06 11:27'
comments: true
share: true
---
<script src="https://karttur.github.io/common/assets/js/karttur/togglediv.js"></script>
## Introduction

The script and associated parameter files in this post are customized for running in <span class='app'>Blender</span>. To reproduce the 3D objects presented you first have to load the script file and then sequentially change the <span class='file'>xml</span> file that the script reads and executes. How to load and edit the script file is covered in the post [Python scripting in Blender](../../setup/reprap-blender-python-3d-render/).

## Blender python script

The python script that needs to be pasted in <span class='app'>Blender</span> and that reads the <span class='file'>xml</span> commands and creates the 3D models is available from the url [https://karttur.github.io/reprap/python/blender_spectrometer_design_v061.py](../../python/blender_spectrometer_design_v061.py).

### Spectrometer container AMS

The <span class='file'>xml</span> parameterisation file for the spectrometer container (or box) for the [AMS series of spectrometers](https://karttur.github.io/arduino/sensor/sensor-AS726X-spectrometer/), version 0.61d (see figure) is under the url [https://karttur.github.io/reprap/xml-models/spectro-box-AMS_20210606_v061d.xml](../../xml-models/spectro-box-AMS_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-box-AMS_20210606_v061d.stl](../../stl-models/spectro-box-AMS_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-box-AMS_20210606_v061d.png">
<figcaption>AMS spectrometer container version 0.61d (20210606)</figcaption>
</figure>

### Spectrometer lock

The spectrometer lock <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-lock_20210606_v061d.xml](../../xml-models/spectro-lock_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-lock_20210606_v061d.stl](../../stl-models/spectro-lock_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-lock_20210606_v061d.png">
<figcaption>Spectrometer lock version 0.61d (20210606)</figcaption>
</figure>

### Direct samplers

There are three slightly different direct samplers that can be attached to the spectrometer box, each designed for a specific type of light source:

- LED lights (white/blue)
- xenon lights
- laser (red or green)

#### White/Blue LED light (VIS/fluorescence sensing)

The direct sampler for LED lights (see figure) can in principle be equipped with any standard 5 mm LED bulb, but is intended for either a clear white led for VIS reflectance spectroscopy or a blue LED for fluorescence spectroscopy. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-direct-cyl-led_20210606_v061d.xml](../../xml-models/spectro-direct-cyl-led_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-direct-cyl-led_20210606_v061d.stl](../../stl-models/spectro-direct-cyl-led_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-direct-cyl-led_20210606_v061d.png">

<figcaption>Spectrometer attachment for direct sampling with LED light version 0.61d (20210606)</figcaption>
</figure>

#### Xenon light (VIS-NIR sensing)

The direct sampler for VIS-NIR reflectance with xenon lights (see figure) differs from the LED ditto above only in the front side of the bulb hoder. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-direct-cyl-xenon_20210606_v061d.xml](../../xml-models/spectro-direct-cyl-xenon_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-direct-cyl-xenon_20210606_v061d.stl](../../stl-models/spectro-direct-cyl-xenon_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-direct-cyl-xenon_20210606_v061d.png">
<figcaption>Spectrometer attachment for direct sampling with xenon light version 0.61d (20210606)</figcaption>
</figure>

#### Red laser (NIR Raman spectroscopy)

The direct sampler for NIR Raman reflectance spectroscopy with a red laser (see figure) differs slightly for the bulb fitting compared to the above samplers. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-direct-cyl-red-laser_20210606_v061d.xml](../../xml-models/spectro-direct-cyl-red-laser_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-direct-cyl-red-laser_20210606_v061d.stl](../../stl-models/spectro-direct-cyl-red-laser_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-direct-cyl-red-laser_20210606_v061d.png">
<figcaption>Spectrometer attachment for direct sampling with red laser version 0.61d (20210606)</figcaption>
</figure>

### Grind samplers

The controlled solid (grind) sampler resembles the direct sampler, but with a longer cylinder and a sample holder that fits into the lower half of the cylinder. This gives a more controlled light environment compared to direct samplers. Additionally the use of standardized reference samples can be used for instrument calibration in direct association with the sensing. The controlled grind sampler thus comes in the same versions as the solid sampler.

#### White/Blue LED light (VIS/fluorescence sensing)

The direct sampler for LED lights (see figure) can in principle be equipped with any standard 5 mm LED light, but is intended for either a clear white led for VIS reflectance spectroscopy or a blue LED for fluorscence spectroscopy.  The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-solid-cyl-led_20210606_v061d.xml](../../xml-models/spectro-solid-cyl-led_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-solid-cyl-led_20210606_v061d.stl](../../stl-models/spectro-solid-cyl-led_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-solid-cyl-led_20210606_v061d.png">

<figcaption>Spectrometer attachment for grind (solid) VIS reflectance sampling with LED light version 0.61d (20210606)</figcaption>
</figure>

#### Xenon light (VIS-NIR sensing)

The grind sampler for VIS-NIR reflectance with xenon lights (see figure) differs from the LED ditto above only in the front side of the bulb hoder. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-solid-cyl-xenon_20210606_v061d.xml](../../xml-models/spectro-solid-cyl-xenon_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-solid-cyl-xenon_20210606_v061d.stl](../../stl-models/spectro-solid-cyl-xenon_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-solid-cyl-xenon_20210606_v061d.png">
<figcaption>Spectrometer attachment for girnd (solid) sampling with xenon light version 0.61d (20210606)</figcaption>
</figure>

#### Red/green laser (NIR Raman spectroscopy)

The grind sampler for NIR Raman reflectance spectroscopy with laser (see figure) differs slightly for the bulb fitting compared to the above samplers. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-solid-cyl-red-laser_20210606_v061d.xml](../../xml-models/spectro-solid-cyl-red-laser_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-solid-cyl-red-laser_20210606_v061d.stl](../../stl-models/spectro-solid-cyl-red-laser_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-solid-cyl-red-laser_20210606_v061d.png">
<figcaption>Spectrometer attachment for grind sampling with laser version 0.61d (20210606)</figcaption>
</figure>

### Cuvette samplers

All cuvette samplers are built from two pieces, the cuvette holder, and the foundation that attach to the spectrometer container. The foundation is the same for all cuvette holders; the cuvette sampler comes in 5 different versions, customized for different light sources:

- White LED light
- Blue LED light
- xenon light
- Red laser
- Green laser

#### Cuvette foundation

The cuvette foundation forms a bridge between the spectrometer container and the specific cuvette holder, where the TRX connector sits in the foundation. The <span class='file'>xml</span> parameterisation file for the cuvette foundation is under the url [https://karttur.github.io/reprap/xml-models/spectro-cuvette-trx_20210606_v061d.xml](../../xml-models/spectro-cuvette-trx_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-cuvette-trx_20210606_v061d.stl](../../stl-models/spectro-cuvette-trx_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-cuvette-trx_20210606_v061d.png">
<figcaption>Spectrometer cuvette sampler foundation version 0.61d (20210606)</figcaption>
</figure>

#### Front light (sensing of opaque liquids)

Light supplied from the front (same side as spectrometer) is only of interest for opaque liquids. As the standard AMS breakout boards come with a white LED mounted, the front light cuvette sampler can be used with this light. The front light cuvette sampler thus has no light source of its own. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-cuvette-front_20210606_v061d.xml](../../xml-models/spectro-cuvette-front_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-cuvette-front_20210606_v061d.stl](../../stl-models/spectro-cuvette-front_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-cuvette-front_20210606_v061d.png">

<figcaption>Spectrometer Cuvette sampler for VIS absorbance sampling with LED light version 0.61d (20210606)</figcaption>
</figure>

#### White LED back light (VIS absorbance of transparent liquids)

The cuvette absorbance sampler for transparent liquids comes in two version, for LED and xenon bulbs. The LED version can in principle hold any standard 5 mm LED, but is intended for a white LED (~ 350 to 800 nm) and absorbance spectroscopy in VIS. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-cuvette-back-led_20210606_v061d.xml](../../xml-models/spectro-cuvette-back-led_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-cuvette-back-led_20210606_v061d.stl](../../stl-models/spectro-cuvette-back-led_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-cuvette-back-led_20210606_v061d.png">

<figcaption>Spectrometer Cuvette sampler for VIS absorbance sampling with LED light version 0.61d (20210606)</figcaption>
</figure>

#### Xenon back light (VIS-NIR absorbance of transparent liquids)

The cuvette sampler absorbance xenon version <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-cuvette-xenon_20210606_v061d.xml](../../xml-models/spectro-cuvette-xenon_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-cuvette-xenon_20210606_v061d.stl](../../stl-models/spectro-cuvette-xenon_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-cuvette-xenon_20210606_v061d.png">

<figcaption>Spectrometer Cuvette sampler for VIS absorbance sampling with LED light version 0.61d (20210606)</figcaption>
</figure>

#### Blue led side light (VIS-NIR fluorescence of transparent liquids)

A blue LED light source can be used for fluorescence spectroscopy. Applied to transparent samples in a cuvette it is better to shine the light 90 degrees from the sensor. The cuvette sample for fluorescence thus have the LED mounted on the side of the cuvette holder. The LED holder as such can hold any 5 mm standard LED. The <span class='file'>xml</span> parameterisation file is under the url [https://karttur.github.io/reprap/xml-models/spectro-cuvette-blue-led_20210606_v061d.xml](../../xml-models/spectro-cuvette-blue-led_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-cuvette-blue-led_20210606_v061d.stl](../../stl-models/spectro-cuvette-blue-led_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-cuvette-blue-led_20210606_v061d.png">

<figcaption>Spectrometer Cuvette sampler for fluorescence spectroscopy with blue LED version 0.61d (20210606)</figcaption>
</figure>

#### Green laser side light (VIS-NIR Raman spectroscopy of transparent liquids)

Also Raman spectroscopy with laser light is preferably applied sideways. The <span class='file'>xml</span> parameterisation file for the green laser, including a 5v dc-dc stepup board, is under the url [https://karttur.github.io/reprap/xml-models/spectro-cuvette-green-laser_20210606_v061d.xml](../../xml-models/spectro-cuvette-green-laser_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-cuvette-green-laser_20210606_v061d.stl](../../stl-models/spectro-cuvette-green-laser_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-cuvette-green-laser_20210606_v061d.png">

<figcaption>Spectrometer Cuvette sampler for Raman spectroscopy with green laser version 0.61d (20210606)</figcaption>
</figure>

#### Red laser side light (VIS-NIR Raman spectroscopy of transparent liquids)

The <span class='file'>xml</span> parameterisation file for red laser absorbance spectroscopy is under the url [https://karttur.github.io/reprap/xml-models/pectro-cuvette-red-laser_20210606_v061d.xml](../../xml-models/spectro-cuvette-red-laser_20210606_v061d.xml). The <span class='file'>stl</span> 3D print file is under [https://karttur.github.io/reprap/stl-models/spectro-cuvette-red-laser_20210606_v061d.stl](../../stl-models/spectro-cuvette-red-laser_20210606_v061d.stl).

<figure>
<img src="../../images/spectro-cuvette-red-laser_20210606_v061d.png">

<figcaption>Spectrometer Cuvette sampler for Raman spectroscopy with red laser version 0.61d (20210606)</figcaption>
</figure>
