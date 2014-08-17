"""
This module helps to iterate through 
all referenced files in the current maya scene,
check for updates and replace with the new version.
"""

__author__ = "Vahan Sosoyan"
__copyright__ = "Copyright 2014, Triada Studio"
__license__ = "GPL"
__version__ = "1.4"
__email__ = "sosoyan@gmail.com"

import maya.cmds as cmds
import os, glob, sys
import maya.OpenMaya as api

def refCheckUpdateDialog(newVersionsList):
    newVersionsCount = len(newVersionsList)
    refAssetsString = ""
    newVersionsNums= []

    for i in newVersionsList:
        newVersionsNums.append(newVersionsList.index(i)+1)

    newVersionsNumsList=[]

    for i,k in zip(newVersionsNums,newVersionsList):
        newVersionsNumsList.append(str(i)+"."+str(k))

    for i in newVersionsNumsList:
        refAssetsString += "%s\n"%i

    return cmds.confirmDialog(title="Check for Updates",
                              message="%s new versions of asset references has been found\n\n%s\n\
                              Note: It's recommended to up version your scene \
                              after updating your assets!"%(newVersionsCount,refAssetsString),
                              button=["Update by one","Update All","Skip by one", "Cancel"],
                              defaultButton="Update",
                              cancelButton="Cancel",
                              dismissString="Cancel",
                              icn="information")

def refsUpdateChecker(ifLoaded,topRef):
    def uniq(input):
        output = []
        for x in input:
            if x not in output:
                output.append(x)
        return output

    def compare(src, test):
        if len(src) != len(test):
            return
        diffmap = [0]*len(src)
        count = 0
        for i, c in enumerate(src):
            if not c == test[i]:
                count = count+1
                diffmap[i] = 1
        return diffmap

    refSel = cmds.ls(rf=1)
    
    if ifLoaded==1 and topRef==1:
        refLoaded = []
        for i in refSel:
            refLoaded.append(cmds.referenceQuery(i, il=1))
        refListLoaded = [d for (d, remove) in zip(refSel, refLoaded) if remove]  
        refListDup=[]
        for i in refListLoaded:
            refListDup.append(cmds.referenceQuery(i, rfn=1, tr=1))
        refList = uniq(refListDup)
    elif ifLoaded==1 and topRef==0:   
        refLoaded = []
        for i in refSel:
            refLoaded.append(cmds.referenceQuery(i, il=1))
        refListLoaded = [d for (d, remove) in zip(refSel, refLoaded) if remove]
        refList = refListLoaded
    elif ifLoaded==0 and topRef==1:
        refListDup=[]
        for i in refSel:
            refListDup.append(cmds.referenceQuery(i, rfn=1, tr=1))
        refList = uniq(refListDup)
    else:
        refList = refSel

    refFilePaths = []

    for i in refList:
        refFilePaths.append(cmds.referenceQuery(i, f=1))

    refFileVersionList = []

    for i in refFilePaths:
        refFileDirList = os.path.abspath(os.path.join(i, os.pardir))
        refFileList = os.path.splitext(os.path.basename(i))[0]
        refFileName = refFileList[:refFileList.rfind("v")+1]
        refFileVersionList.append(glob.glob("%s/%s*"%(refFileDirList,refFileName)))

    refFileNewVersionPaths=[]
    
    for i in refFileVersionList:
        refFileNewVersionPaths.append(i[-1])

    refFileFullName = []
    refFileNewVersionFullName = []

    for i in refFilePaths:
        refFileFullName.append(os.path.basename(i))

    for i in refFileNewVersionPaths:
        refFileNewVersionFullName.append(os.path.basename(i))

    indexList = compare(refFileNewVersionFullName,refFileFullName)
    indices = [i for i, x in enumerate(indexList) if x == 1]

    refListDif  = []
    refFileNewVersionPathsDif=[]

    for i in indices:
        refListDif.append(refList[i])
        refFileNewVersionPathsDif.append(refFileNewVersionPaths[i])

    return list([refListDif, refFileNewVersionPathsDif, refList])

def refsUpdater(**kwargs):
    ifLoaded = kwargs.setdefault("il",1)
    topRef = kwargs.setdefault("tr",1)  
    refsUpdateCheckerOutput = refsUpdateChecker(ifLoaded,topRef)
    
    def mainRefsUpdater():
        if len(refsUpdateCheckerOutput[2]) > 0:
            if len(refsUpdateCheckerOutput[1]) > 0:
                refCheckUpdateDialogAnswer = refCheckUpdateDialog(refsUpdateCheckerOutput[1])
                if refCheckUpdateDialogAnswer == "Update by one":
                        cmds.file(refsUpdateCheckerOutput[1][0],lr=refsUpdateCheckerOutput[0][0])
                        del refsUpdateCheckerOutput[0][0]
                        del refsUpdateCheckerOutput[1][0]
                        mainRefsUpdater()
                elif refCheckUpdateDialogAnswer == "Update All":
                        for i,k in zip(refsUpdateCheckerOutput[0],refsUpdateCheckerOutput[1]):
                            cmds.file(k,lr=i)
                elif refCheckUpdateDialogAnswer == "Skip by one": 
                        del refsUpdateCheckerOutput[0][0]
                        del refsUpdateCheckerOutput[1][0]
                        mainRefsUpdater()
                else:
                    pass
            else:
                sys.stdout.write("// Info: Assets are updated.")
        else:
            sys.stdout.write("// Info: There are no any asset references in the current scene.")
    mainRefsUpdater()

def refsUpdaterExe(self):
    refsUpdater(il=1,tr=1)

def refsUpdaterCallback():
    api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, refsUpdaterExe)
