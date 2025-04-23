import sys
import os
import maya.cmds as cmds
from functools import partial
from importlib import reload

def reload_ui(*args):
    import option_menu
    reload(option_menu)
    option_menu.option_menu_ui()

def call_skinCluster(*args):
    import skinClusterManager 
    reload(skinClusterManager)

def option_menu_ui():

    if cmds.menu("ToolKit", exists=True):
        cmds.deleteUI("ToolKit")
    cmds.menu("ToolKit", label="ToolKit ", tearOff=True, parent="MayaWindow")

    cmds.menuItem(label="   Settings", subMenu=True, tearOff=True, boldFont=True)
    cmds.menuItem(label="   Reload UI", command=reload_ui)

    cmds.setParent("..", menu=True)
    cmds.menuItem(dividerLabel="\n ", divider=True)


    cmds.menuItem(label="   Rigging", subMenu=True, tearOff=True, boldFont=True)
    cmds.menuItem(label="   SkinCluster Manager", command=call_skinCluster)


    cmds.setParent("..", menu=True)