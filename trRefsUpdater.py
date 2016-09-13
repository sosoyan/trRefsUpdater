"""
This module helps to iterate through
all referenced files in the current maya scene,
check for updates and replace with the new version.
"""

__author__ = "Vahan Sosoyan"
__copyright__ = "Copyright 2016"
__license__ = "GPL"
__version__ = "2.0"

import maya.cmds as cmds
import maya.utils as utils
import os, glob, sys, re
import maya.OpenMaya as api

class RefNode(object):
    def __init__(self, name, path, isLoaded):
        self.name = name
        self.path = path
        self.isLoaded = isLoaded
        self.fileName = os.path.splitext(os.path.basename(path))[0]
        self.version = re.search(r".v\d+", self.fileName).group()[2:]
        
        self.updatePath = glob.glob(self.path.replace(self.version, "*"))[-1].replace("\\", "/")
        self.updateFileName = os.path.splitext(os.path.basename(self.updatePath))[0]
        self.updateVersion = re.search(r".v\d+", self.updateFileName).group()[2:]

        self.hasUpdate = (self.updatePath != self.path)

    def update(self):
        if self.isLoaded and self.hasUpdate:
            cmds.file(self.updatePath, lr=self.name, lrd="topOnly")

def refCheckUpdateDialog(newVersionsNames, newVersionsList):

    newVersionsCount = len(newVersionsList)
    refAssetsString = ""
    note = "Note: It's recommended to up version your scene after updating your assets!"
    newVersionsNums= []

    for i in range(0,newVersionsCount):
        newVersionsNums.append(i+1)

    newVersionsNumsList=[]

    for i,j,k in zip(newVersionsNums,newVersionsNames,newVersionsList):
            newVersionsNumsList.append(str(i)+". "+str(j)+str(" update to")+"\n"+str(k)+"\n")
    for i in newVersionsNumsList:
        refAssetsString += "%s\n"%i

    return cmds.confirmDialog(title="TRIADA Check for Updates v2.0",
                              message="%s new versions of asset references have been found\n\n%s\n%s"
                              %(newVersionsCount,refAssetsString,note),
                              button=["Update All", "Update by One","Skip by One", "Cancel"],
                              defaultButton="Update",
                              cancelButton="Cancel",
                              dismissString="Cancel",
                              icn="information")

def getRefNodesList():
    # Get reference nodes
    refSel = [i for i in cmds.ls(rf=1) if "_UNKNOWN_REF_NODE_" not in i]

    # Remove ghost ref nodes from selection
    for i in refSel:
        try:
            cmds.referenceQuery(i, il=1)
        except:
            refSel.remove(i)

    # Create refNodes objects list
    refNodes = []
    for i in refSel:
        name = cmds.referenceQuery(i, rfn=1)
        path = cmds.referenceQuery(i, f=1, wcn=1)
        isLoaded = cmds.referenceQuery(i, il=1)

        # Append only versioned ref nodes
        fileName = os.path.splitext(os.path.basename(path))[0]
        if re.search(r".v\d+", fileName) != None:
            refNodes.append(RefNode(name, path, isLoaded))
    return refNodes

def refsUpdater(*args):
    nodeList = getRefNodesList()
    nodeUpdateList = [i for i in nodeList if (i.hasUpdate and i.isLoaded)]
    updatedList, skippedList = [], []

    def updater():
        if len(nodeUpdateList) > 0:
            nameList = [i.name for i in nodeUpdateList if (i.hasUpdate and i.isLoaded)]
            updatePathList = [i.updatePath for i in nodeUpdateList if (i.hasUpdate and i.isLoaded)]
            dialog = refCheckUpdateDialog(nameList, updatePathList)

            if dialog == "Update All":
                for i in nodeUpdateList:
                    i.update()
                    updatedList.append(i.name)

            elif dialog == "Update by One":
                nodeUpdateList[0].update()
                updatedList.append(nodeUpdateList[0].name)
                del nodeUpdateList[0]
                updater()

            elif dialog == "Skip by One":
                skippedList.append(nodeUpdateList[0].name)
                del nodeUpdateList[0]
                updater()
        else:
            sys.stdout.write("// Info: All assets are up to date.\n")
    updater()

    # Unload if needed
    for i in nodeList:
        loaded = cmds.referenceQuery(i.name, il=1)
        if not loaded and i.isLoaded:
            cmds.file(i.path, loadReference=i.name)

    # Status Message
    if len(updatedList) > 0:
        sys.stdout.write("// Info: %s updated.\n"%(", ".join(updatedList)))
    if len(skippedList) > 0:
        sys.stdout.write("// Info: %s skipped.\n"%(", ".join(skippedList)))

if __name__ != "__main__":
    api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, refsUpdater)
