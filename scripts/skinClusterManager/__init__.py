"""

WIP

"""
from importlib import reload
import skinClusterManager.ui as ui
reload(ui)


try:
    skinClusterManagerInstance.close()
except:
    pass

skinClusterManagerInstance = ui.SkinClusterManager()
skinClusterManagerInstance.show()