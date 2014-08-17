###trRefsUpdater
Copyright 2014, Triada Studio

by Vahan Sosoyan sosoyan@gmail.com

===

This module helps to iterate through all referenced files in the current maya scene, check for updates and replace with the new versions.

###Usage

It can be used in maya as custom python callback as well as seperate command.

1.To activate custom maya callback which enables interactive notifications after every time you open maya scene, just add trRefsUpdater.py and userSetup.py to your maya scripts directory, or if you already have userSetup.py, add this lines above.

```bash
import maya.utils as utils
import trRefsUpdater

utils.executeDeferred('trRefsUpdater.refsUpdaterCallback()')
```

2.To use as seperate command see refsUpdater() function.

```bash
trRefsUpdater.refsUpdater()
```
it can be used with custom flags `il` (if loaded) and `tr` (top reference) to fit in your pipeline.

```bash
refsUpdater([il=boolean],[tr=boolean])
```

**NOTE:** by default both flags are True.

====
