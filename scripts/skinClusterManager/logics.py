import maya.cmds as cmds
import maya.api.OpenMaya as om2



"""
Still Workin in progress
"""


def check_skincluster_existance():
    sel = cmds.ls(sl=True)
    relatives = cmds.listRelatives(sel, ad=True, shapes=True)
    if len(relatives) >= 2:
        skin_clusters = cmds.listConnections(relatives[0], type="skinCluster")
        print(f"Input connections: {skin_clusters}")
        if skin_clusters:
            om2.MGlobal.displayInfo(f"SkinClusters found: {skin_clusters}")
            return skin_clusters
        else:
            om2.MGlobal.displayError("No Skinclusters found in the selection.")
     
    else:
        om2.MGlobal.displayError("No Skinclusters found in the selection.")

def merge_skin_clusters(target_skinCluster, source_skinCluster):
    if not cmds.objExists(target_skinCluster) or cmds.objectType(target_skinCluster) != "skinCluster" or not cmds.objExists(source_skinCluster) or cmds.objectType(source_skinCluster) != "skinCluster":
        om2.MGlobal.displayError("One or both nodes do not exist or are not skinCluster nodes.")
        return
    
    list_target_input_connections = cmds.listConnections(target_skinCluster, connections=True, source=True, destination=False, shapes=True)
    list_source_input_connections = cmds.listConnections(source_skinCluster, connections=True, source=True, destination=False, shapes=True)
    
    for e, lists in enumerate([list_target_input_connections, list_source_input_connections]):
        connections_accepted =[
            ".input[0].inputGeometry",
            ".originalGeometry[0]"
        ]
        i = 0
        valid_connections = []
        while i < len(lists):
            for connection in connections_accepted:
                if connection in lists[i]:
                    valid_connections.append([lists[i], lists[i+1]])
                    i += 2
                else:
                    i += 1
        if e == 0:
            target_valid_connections = valid_connections
        else:
            source_valid_connections = valid_connections

    for i, connection in enumerate(source_valid_connections):
        if "originalGeometry" in connection[0]:
            origin_shape = connection[1] 

    cmds.connectAttr(f"{origin_shape}.worldMesh[0]", f"{target_skinCluster}.input[0].inputGeometry", force=True)
    cmds.connectAttr(f"{origin_shape}.outMesh", f"{target_skinCluster}.originalGeometry[0]", force=True)
    cmds.connectAttr(f"{target_skinCluster}.outputGeometry[0]", f"{source_skinCluster}.input[0].inputGeometry", force=True)


def rebuild_skinCluster(rebuildable_skinCluster, mesh="new"):
    if not cmds.objExists(rebuildable_skinCluster) or cmds.objectType(rebuildable_skinCluster) != "skinCluster":
        om2.MGlobal.displayError("The node does not exist or is not a skinCluster node.")
        return
    
    list_rebuildable_connections = cmds.listConnections(rebuildable_skinCluster, connections=True, source=True, destination=True, shapes=True)
    print(list_rebuildable_connections)

    connections_accepted =[
        ".input[0].inputGeometry",
        ".originalGeometry[0]",
        ".outputGeometry[0]"
    ]
    i = 0
    valid_connections = []
    while i < len(list_rebuildable_connections):
        for connection in connections_accepted:
            if connection in list_rebuildable_connections[i]:
                valid_connections.append([list_rebuildable_connections[i], list_rebuildable_connections[i+1]])
                i += 1
                continue
        i += 1

    for i, connection in enumerate(valid_connections):
        if "originalGeometry" in connection[0]:
            origin_shape = connection[1] 
        elif "outputGeometry" in connection[0]:
            output_shape = connection[1]
        elif "inputGeometry" in connection[0]:
            input_shape = connection[1]
    
    if cmds.objectType(input_shape) == "mesh" and cmds.objectType(output_shape) == "mesh":
        om2.MGlobal.displayInfo("The skinCluster is already rebuilt.")
        return
    else:
        if mesh == "new":
            if cmds.objectType(input_shape) == "skinCluster" and cmds.objectType(output_shape) == "mesh": 
                cmds.connectAttr(f"{input_shape}.outputGeometry[0]", f"{output_shape}.inMesh", force=True)
                duplicate = cmds.duplicate(output_shape, name=f"{output_shape}Rebuilt")
                print(duplicate)


    
rebuild_skinCluster("skinCluster1")
