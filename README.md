

###trRefsUpdater

This module helps to iterate through all referenced files in the current maya scene, check for updates and replace with the new version

###Usage

It can be used in maya as custom python callback as well as seperate command.

To activate custom maya callback which enables interactive notifications after every time you open maya scene. Just add userSetup.py and trRefsUpdater.py to your maya scripts directory, or if you already have userSetup.py, just add this lines above.

```bash
import maya.utils as utils
import trRefsUpdater

utils.executeDeferred('trRefsUpdater.refsUpdaterCallback()')
```


To use as seperate command use refsUpdater() function.

```bash
trRefsUpdater.refsUpdater()
```

by default it watches for only if loaded and top referenced files but if want to iterate through all files use arguments.

```bash
refsUpdater(il=0,tr=0)
```


====
