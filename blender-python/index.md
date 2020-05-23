---
layout: page
title: Blender models (python)
excerpt: "Blender 3D models created with Python scripting"
image: std-trmm-3b43v7-precip_3B43_trmm_2001-2016_A
search_omit: true
---

<ul class="post-list">
{% for post in site.categories.blender-python reversed %}
  <li><article><a href="{{ site.url }}{{ post.url }}">{{ post.title }} <span class="entry-date"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time></span>{% if post.excerpt %} <span class="excerpt">{{ post.excerpt | remove: '\[ ... \]' | remove: '\( ... \)' | markdownify | strip_html | strip_newlines | escape_once }}</span>{% endif %}</a></article></li>
{% endfor %}
</ul>
