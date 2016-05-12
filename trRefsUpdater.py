"""
This module helps to iterate through 
all referenced files in the current maya scene,
check for updates and replace with the new version.
"""

__author__ = "Vahan Sosoyan"
__copyright__ = "Copyright 2014, Triada Studio"
__license__ = "GPL"
__version__ = "1.6.1"

import maya.cmds as cmds
import os, glob, sys
import maya.OpenMaya as api

def refCheckUpdateDialog(newVersionsNames,newVersionsList):

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

    return cmds.confirmDialog(title="TRIADA Check for Updates",
                              message="%s new versions of asset references has been found\n\n%s\n%s"
                              %(newVersionsCount,refAssetsString,note),
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

    for i in refSel:
        if "_UNKNOWN_REF_NODE_" in i:
            refSel.remove(i)
    
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
        refFilePaths.append(cmds.referenceQuery(i, f=1, wcn=1))

    refFileVersionList = []

    for i in refFilePaths:
        refFileDirList = os.path.abspath(os.path.join(i, os.pardir))
        refFileList = os.path.splitext(os.path.basename(i))[0]
        refFileExt = os.path.splitext(os.path.basename(i))[1]
        refFileName = refFileList[:refFileList.rfind("_v")+2]+"*%s"%refFileExt
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
    callBack = kwargs.setdefault("cb",0)
    loadRefDepth = kwargs.setdefault("lrd","topOnly")
    refsUpdateCheckerOutput = refsUpdateChecker(ifLoaded,topRef)
    updateList = []
    skipList = []
    def mainRefsUpdater(callBack):
        if len(refsUpdateCheckerOutput[2]) > 0:
            if len(refsUpdateCheckerOutput[1]) > 0:
                refCheckUpdateDialogAnswer = refCheckUpdateDialog(refsUpdateCheckerOutput[0],refsUpdateCheckerOutput[1])
                if refCheckUpdateDialogAnswer == "Update by one":
                    cmds.file(refsUpdateCheckerOutput[1][0],lr=refsUpdateCheckerOutput[0][0],lrd=loadRefDepth)
                    updateList.append(refsUpdateCheckerOutput[0][0])
                    del refsUpdateCheckerOutput[0][0]
                    del refsUpdateCheckerOutput[1][0]
                    mainRefsUpdater(callBack)
                elif refCheckUpdateDialogAnswer == "Update All":
                    for i in refsUpdateCheckerOutput[0]:
                        updateList.append(i)
                    for i,k in zip(refsUpdateCheckerOutput[0],refsUpdateCheckerOutput[1]):
                        cmds.file(k,lr=i,lrd=loadRefDepth)
                    if len(skipList) == 0:
                        sys.stdout.write("// Info: %s updated."%(", ".join(updateList)))
                    else:
                        sys.stdout.write("// Info: %s updated | %s skipped."
                        %((", ".join(updateList)),(", ".join(skipList))))
                elif refCheckUpdateDialogAnswer == "Skip by one":
                    skipList.append(refsUpdateCheckerOutput[0][0])
                    del refsUpdateCheckerOutput[0][0]
                    del refsUpdateCheckerOutput[1][0]
                    mainRefsUpdater(callBack)
                elif refCheckUpdateDialogAnswer == "Cancel":
                    for i in refsUpdateCheckerOutput[0]:
                        skipList.append(i)
                    if len(updateList) == 0:
                        sys.stdout.write("// Info: %s skipped."%(", ".join(skipList)))
                    else:
                        sys.stdout.write("// Info: %s updated | %s skipped."
                        %((", ".join(updateList)),(", ".join(skipList))))
            else:
                if len(updateList)>0 or len(skipList)>0:
                    if len(updateList) == 0:
                            sys.stdout.write("// Info: %s skipped."%(", ".join(skipList)))
                    elif len(skipList) == 0:
                            sys.stdout.write("// Info: %s updated."%(", ".join(updateList)))
                    else:
                        sys.stdout.write("// Info: %s updated | %s skipped."
                        %((", ".join(updateList)),(", ".join(skipList))))
                else:
                    sys.stdout.write("// Info: All assets are up to date.")
        else:
            if callBack == 0:
                cmds.warning("There are no any referenced assets in the current scene.")
    mainRefsUpdater(callBack)

def refsUpdaterExe(*args):
    refsUpdater(il=1,tr=1,lrd="topOnly",cb=1)

def refsUpdaterCallback():
    api.MSceneMessage.addCallback(api.MSceneMessage.kAfterOpen, refsUpdaterExe)
