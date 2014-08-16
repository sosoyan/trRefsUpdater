

###trRefsUpdater

This module helps to iterate through all referenced files in the current maya scene, check for updates and replace with the new version

###Usage

It can be used in maya as custom python callback as well as seperate command.

1. You can activate custom maya callback through your userSetup.py which enables you to get interactive notifications after every time you open maya scene. Just add userSetup.py and trRefsUpdater.py to your maya scripts directory, or if you already have userSetup.py, just add this lines above.

```bash
import maya.utils as utils
import trRefsUpdater

utils.executeDeferred('trRefsUpdater.refsUpdaterCallback()')
```

2. You can use refsUpdater() command to add to shelves or custom menus
====
