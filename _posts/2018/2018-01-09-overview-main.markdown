---
layout: post
title: Karttur GitHub repository overview
modified: '2018-01-09 T18:17:25.000Z'
categories: overview
excerpt: "Overview of Karttur´s GitHub site for blogs, articles and manuals"
tags:
  - Blog setup
  - IDE setup
  - DB setup
  - GIS installations
  - macOS
image: avg-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
date: '2018-01-09 11:27'
comments: true
share: true
---
**Contents**
\- [Scaffolding](#scaffolding)
\- [Repositories](#repositories)
  \- [overview](#overview)
  \- [setup-blog](#setup-blog)
  \- [setup-github](#setup-github)
  \- [setup-theme-blog](#setup-theme-blog)
  \- [setup-ide](#setup-ide)

This blog is an attempt to create an overview of the contents in Karttur's GitHub site. The site is organized in repositories, with each repository containing a blog, and some containing program codes. You can use the top menu to get to the different repositories, or the links in the descriptions of the content of each repository below.

## Scaffolding

```bash
karttur/
├── overview/
|    └── blog/
|        └──                          # empty
|    └── overview/
|        └── overview-main            # this page
├── setup-blog/
|    └── Set up blog tools            # tutorial on Jekyll and Atom
├── setup-github/
|    └── Set up GitHub                # tutorial on markdown and GitHub
├── setup-theme-blog/
|    └── blog/
|        └── hide-show-div            # Hide/show code with javascript
|    └── setup-blog/
|        ├── Set up Jekyll theme blog # Select, edit and publish Jekyll Theme
|        └── Theme Setup              # The So Simple Theme instructions
├── setup-ide/
|    └── blog/
|        └──                          # empty
|    └── ide-setup/     
|        ├── Install Anaconda         # Install Anaconda Python package on macOS
|        ├── Setup Eclipse with PyDev # Install Eclipse and set up with Anaconda
|        ├── Install PostgreSQL       # Install PostgreSQL and PostGIG on macOS
|        ├── Connect PostgreSQL       # psycopg2 connect PostgreSQL and Python  
|        ├── PostgreSQL xml setup     # Setup db schema & tables using xml
|        └── GDAL, QGIS and GRASS     # Install GDAL, QGIS and GRASS on macOS
```
## Repositories

### overview

The overview repository only contains web-pages.

### setup-blog

The repository [Setup-blog](https://karttur.github.io/setup-blog/) contains a manual on how that very page was created by using Jekyll and the default Theme minima. The page also introduces using the text editor <span class='app'>Atom</span> for editing markdown files. The GitHub repository contains the full code under the branch 'gh-pages'. It might be useful to follow the manual to set up your very first Jekyll blog.

Url links:
* [front web page](https://karttur.github.io/setup-blog/)
* [GitHub repository](https://github.com/karttur/setup-blog/tree/gh-pages)

### setup-github

Also the repository [Setup-github](https://karttur.github.io/setup-github/) contains a single web-page created using Jekyll, but without any template Theme. The page is an introductory manual on how to publish a web site with blogs on GitHub.com using <span class='app'>GitHub desktop.app</span>. The GitHub repository contains the full code under the branch 'gh-pages'. It might be useful for learning a bit about markdown and publishing Jekyll generated web-pages on GitHub.

Url links:
* [front web-page](https://karttur.github.io/setup-github/)
* [GitHub repository](https://github.com/karttur/setup-github/tree/gh-pages)

### setup-theme-blog

After having tried out creating web-pages using Jekyll, learnt a bit about markdown and editing the markdown coding system in the text editor Atom, I selected an Open Source Jekyll Theme (So Simple by Michael Rose) as the template for continuing publishing my articles and blogs. The repository [setup-theme-blog](https://karttur.github.io/setup-theme-blog/) contains my step-by-step manual on how I setup the So Simple Theme. The blog contains additional tweaking I have done to the So Simple Theme to make it fit my needs.

Url links:
* [front web-page](https://karttur.github.io/setup-theme-blog/)
* [GitHub repository](https://github.com/karttur/setup-theme-blog/tree/gh-pages)

### setup-ide

The core of the Karttur site is about map making and spatial data processing, especially using satellite images. The repository [setup-ide](https://karttur.github.io/setup-ide/) (ide stands for Integrated Development Environment) covers the installations and setups to create the framework needed for the kind of map making that Karttur does.

Url links:
* [front web-page](https://karttur.github.io/setup-ide/)
* [GitHub](https://github.com/karttur/setup-ide/tree/gh-pages)

Direct links to the installation and setup instructions of different components (primarily for macOS):

* [GIS](https://karttur.github.io/setup-ide/setup-ide/install-gis/) (Install GDAL, QGIS and GRASS)
* [Anaconda](https://karttur.github.io/setup-ide/setup-ide/install-anaconda/) (Install Ananconda Python Interpreter)
* [Eclipse](https://karttur.github.io/setup-ide/setup-ide/install-eclipse/) (Install IDE for Python)
* [PostgreSQL](https://karttur.github.io/setup-ide/setup-ide/install-postgres/) (Install PostgreSQL with PostGIS database)
* [psycopg2](https://karttur.github.io/setup-ide/setup-ide/connect-with-psycopg2/) (connect Python and Postgres using psycopg2)
* [db architecture](https://karttur.github.io/setup-ide/setup-ide/setup-db-karttur/) (create db architecture [schemas and tables] using xml)
