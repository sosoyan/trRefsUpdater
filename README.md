###trRefsUpdater
Copyright 2014, Triada Studio

by Vahan Sosoyan sosoyan@gmail.com

===

This module helps to iterate through all referenced files in the current maya scene, check for updates and replace with the new versions.

![](https://dl.dropboxusercontent.com/u/11663164/shared/trRefsUpdater_Demo.gif)

===

###Installation

Just clone trRefsUpdater.py and userSetup.py to your maya scripts directory, or if you already have userSetup.py, then add this lines above.

```bash
import maya.utils as utils
import trRefsUpdater

utils.executeDeferred('trRefsUpdater.refsUpdaterCallback()')
```

###Usage

It checks for new filename versions of referenced files, after every time you open maya scene and if founds one, will porpose to update them.

Also can be used as seperate command.

```bash
import trRefsUpdater

trRefsUpdater.refsUpdater()
```
Custom `il` (if loaded) and `tr` (top reference) flags are available to make it fit in your pipeline.

```bash
refsUpdater([il=boolean],[tr=boolean])
```

**NOTE:** by default both flags are True.

====
