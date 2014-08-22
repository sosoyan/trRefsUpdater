###trRefsUpdater
Copyright 2014, Triada Studio

by Vahan Sosoyan sosoyan@gmail.com

===

This module helps to iterate through all referenced files in the current maya scene, check for updates and replace with the new versions.

![](https://dl.dropboxusercontent.com/u/11663164/shared/trRefsUpdater_Demo.gif)

===

###Installation

Clone this repo into your maya scripts directory, or if you already have userSetup.py, then add this lines above.

```bash
import maya.utils as utils
import trRefsUpdater

utils.executeDeferred('trRefsUpdater.refsUpdaterCallback()')
```

###Usage

As soon, as you open Maya scene, the callback script will automatically check for new filename versions for all  reference objects in the scene and in case there are any in place, will offer to update them.

Also can be used as seperate command.

```bash
import trRefsUpdater

trRefsUpdater.refsUpdater()
```
Custom `il` ( isLoaded ), `tr` ( topReference ) and `lrd` ( loadReferenceDepth ) flags are available to make it best fit in your pipeline.

```bash
refsUpdater([il=boolean],[tr=boolean],[lrd=string("all","topOnly","none")])
```

**NOTE:** By default `il=True`, `tr=True`, `lrd="topOnly"`

###Release Notes

#### 1.6

- Fixed issue with duplicated reference objects
- Layout improvment of confirm dialog

#### 1.5

- Added better feedback status through script editor for updated or skipped assets
