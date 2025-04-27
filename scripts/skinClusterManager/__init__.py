from importlib import reload
import skinClusterManager.ui as ui
reload(ui)

# In case the UI is already open, close it first
try:
    skinClusterManagerInstance.close()
except:
    pass

# Create a new instance of the SkinClusterManager UI
skinClusterManagerInstance = ui.SkinClusterManager()
skinClusterManagerInstance.show()