import json
import os
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

class CompoundList(QtWidgets.QFrame):
    """
    Compound widget with a button and a list widget.
    """

    def __init__(self, name = "Test", tooltip = "Test"):
        """
        Initialize the CompoundList widget.
        Args:
            name (str): The name of the button.
            tooltip (str): The tooltip for the button.
        """

        super().__init__()
        self.populate(name = name, tooltip = tooltip)
        self.create_layout()

    def populate(self, name, tooltip):
        """
        Populate the widget with a button and a list widget.
        Args:
            name (str): The name of the button.
            tooltip (str): The tooltip for the button.
        """

        self.load_source_btn = QtWidgets.QPushButton(name)
        self.load_source_btn.setToolTip(tooltip)
        self.source_list = MiddleDragListWidget()
    
    def create_layout(self):
        """
        Create the layout for the widget.
        """

        left_top_v_layout = QtWidgets.QVBoxLayout(self) 
        left_top_v_layout.addWidget(self.load_source_btn)   
        left_top_v_layout.addWidget(self.source_list)   

class MiddleDragListWidget(QtWidgets.QListWidget):
    """
    Custom QListWidget that allows dragging items with the middle mouse button.
    """

    def __init__(self, parent=None):
        """
        Initialize the MiddleDragListWidget.
        Args:
            parent (QWidget): The parent widget.
        """
        super(MiddleDragListWidget, self).__init__(parent)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def mousePressEvent(self, event):
        """
        Handle mouse press events.  
        """
        if event.button() == QtCore.Qt.MiddleButton:
            fake_event = QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonPress,
                event.localPos(),
                event.screenPos(),
                QtCore.Qt.LeftButton,
                QtCore.Qt.LeftButton,
                event.modifiers()
            )
            super(MiddleDragListWidget, self).mousePressEvent(fake_event)

        elif event.button() == QtCore.Qt.LeftButton:
            super(MiddleDragListWidget, self).mousePressEvent(event)
            return
            

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events.   
        """
        super(MiddleDragListWidget, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        """ 
        Handle mouse release events.    
        """
        if event.button() == QtCore.Qt.MiddleButton:
            fake_event = QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonRelease,
                event.localPos(),
                event.screenPos(),
                QtCore.Qt.LeftButton,
                QtCore.Qt.LeftButton,
                event.modifiers()
            )
            super(MiddleDragListWidget, self).mouseReleaseEvent(fake_event)
        else:
            super(MiddleDragListWidget, self).mouseReleaseEvent(event)

class SkinClusterManager(QtWidgets.QDialog):
    """
    SkinCluster Manager UI class.
    This class creates a UI for managing skin clusters in Maya.
    It allows users to load, remove, and combine skin clusters.
    """

    def __init__(self):
        """
        Initialize the SkinClusterManager UI.
        """ 
        super(SkinClusterManager, self).__init__(wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.setWindowTitle("SkinCluster Manager")
        self.setMinimumSize(700, 400)

        # Get the path to the current script directory only works if .mod is set correctly
        self.json_path = os.path.join(os.path.dirname(__file__), "styleSheet.json")

        self.svg_path = os.path.join(os.path.dirname(__file__), "images.json")

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.apply_stylesheet()

    def create_widgets(self):
        """ 
        Create the widgets for the UI.
        """  

        self.skincluster_text = QtWidgets.QLabel("SkinCluster Manager") 
        self.skincluster_text.setObjectName("skincluster_text")    
        self.help_button = QtWidgets.QPushButton()
        help_button_logo = self.get_svg("help_button")

        self.help_button.setIcon(QtGui.QPixmap(":help.png"))
        self.help_button.setIconSize(QtCore.QSize(20, 20))
        self.help_button.setToolTip("Help")
        self.help_button.setObjectName("help_button")

        self.div1 = QtWidgets.QFrame()
        self.div1.setFrameShape(QtWidgets.QFrame.HLine)
        self.div1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.div1.setObjectName("divider_line")

        self.load_source = CompoundList(name = "Load Source", tooltip = "Load source skin clusters")
        
        self.right_btn = QtWidgets.QPushButton()
        arrow_icon = self.get_svg("arrow_forward")
        self.right_btn.setIcon(arrow_icon)
        self.right_btn.setToolTip("Move selected source skin clusters to target")
        self.left_btn = QtWidgets.QPushButton()
        arrow_icon = self.get_svg("arrow_back")
        self.left_btn.setIcon(arrow_icon)
        self.left_btn.setToolTip("Move selected target skin clusters to source")

        self.target_source = CompoundList(name = "Load Target", tooltip = "Load target skin clusters")

        self.remove_skc = QtWidgets.QPushButton("Remove SkinCluster")
        self.remove_skc.setToolTip("Remove selected skin clusters")
        self.new_mesh_radio = QtWidgets.QRadioButton()
        self.new_mesh_radio.setText("New Mesh")
        self.target_mesh_radio = QtWidgets.QRadioButton()
        self.target_mesh_radio.setText("Target Mesh")
        self.target_mesh_radio.setChecked(True)
        self.combine_skc = QtWidgets.QPushButton("Combine SkinCluster")
        self.combine_skc.setToolTip("Combine target skin clusters")
        self.rebuild_skc = QtWidgets.QPushButton("Rebuild SkinCluster")
        self.rebuild_skc.setToolTip("Rebuild selected skin clusters")

        self.div2 = QtWidgets.QFrame()
        self.div2.setFrameShape(QtWidgets.QFrame.HLine)
        self.div2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.div2.setObjectName("divider_line")
        self.div2.setStyleSheet("border-width: 1px;")

        self.copyRight_text = QtWidgets.QLabel("Copyright© 2025 Guido Gonzalez. All rights reserved.")
        self.version_text = QtWidgets.QLabel("Version 1.0.0")
        
        

    def create_layout(self):
        """
        Create the layout for the UI.
        """

        top_horizontal_layout_text = QtWidgets.QHBoxLayout()
        top_horizontal_layout_text.addWidget(self.skincluster_text)
        top_horizontal_layout_text.addStretch()
        top_horizontal_layout_text.addWidget(self.help_button)

        middle_top_v_layout = QtWidgets.QVBoxLayout()
        middle_top_v_layout.addStretch()
        middle_top_v_layout.addWidget(self.right_btn)
        middle_top_v_layout.addWidget(self.left_btn)    
        middle_top_v_layout.addStretch()

        top_horizontal_layout = QtWidgets.QHBoxLayout()
        top_horizontal_layout.addWidget(self.load_source)
        top_horizontal_layout.addLayout(middle_top_v_layout)
        top_horizontal_layout.addWidget(self.target_source)    

        bottom_horizontal_layout = QtWidgets.QHBoxLayout()
        bottom_horizontal_layout.addWidget(self.remove_skc)
        bottom_horizontal_layout.addStretch()
        bottom_horizontal_layout.addWidget(self.new_mesh_radio)
        bottom_horizontal_layout.addWidget(self.target_mesh_radio)
        bottom_horizontal_layout.addStretch()
        bottom_horizontal_layout.addWidget(self.combine_skc)
        bottom_horizontal_layout.addWidget(self.rebuild_skc) 

        bottom_text_horizontal_layout = QtWidgets.QHBoxLayout()   
        bottom_text_horizontal_layout.addWidget(self.copyRight_text)
        bottom_text_horizontal_layout.addStretch()
        bottom_text_horizontal_layout.addWidget(self.version_text)
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_horizontal_layout_text)
        main_layout.addWidget(self.div1)
        main_layout.addLayout(top_horizontal_layout)
        main_layout.addLayout(bottom_horizontal_layout)
        main_layout.addWidget(self.div2)
        main_layout.addLayout(bottom_text_horizontal_layout)    

    def create_connections(self):
        """
        Create the connections for the UI.
        """
        self.help_button.clicked.connect(self.open_help)
        self.load_source.load_source_btn.clicked.connect(self.load_source_skin_clusters) 
        self.target_source.load_source_btn.clicked.connect(self.load_target_skin_clusters)
        self.remove_skc.clicked.connect(self.remove_selected_skin_cluster)
        self.right_btn.clicked.connect(self.move_source_to_target)  
        self.left_btn.clicked.connect(self.move_target_to_source)
        self.combine_skc.clicked.connect(self.combine_skin_cluster)
        self.rebuild_skc.clicked.connect(self.rebuild_skin_cluster)

    def get_svg(self, name=None):
        """
        Load SVG icon from the specified path.
        Args:
            name (str): The name of the SVG icon to load.
        Returns:    
            QIcon: The loaded SVG icon.
        """

        if not os.path.exists(self.svg_path):
            print(f"SVG path not found: {self.svg_path}")
            return QtGui.QIcon()

        try:
            with open(self.svg_path, "r") as file:
                svg_dict = json.load(file)

            if name and name in svg_dict:
                svg_data = svg_dict[name]
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(QtCore.QByteArray(svg_data.encode()), "SVG")
                return QtGui.QIcon(pixmap)
            else:
                print(f"SVG with name '{name}' not found in the SVG dictionary.")
                return QtGui.QIcon()
        except Exception as e:
            print(f"Failed to load SVG: {e}")
            return QtGui.QIcon()

    def open_help(self):
        """
        Open the help documentation in the default web browser. 
        """
        url = "https://github.com/GuiidoGC/skin_cluster_manager"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def load_source_skin_clusters(self):
        """
        Load source skin clusters into the list widget.
        """
        count = self.load_source.source_list.count()
        self.load_source.source_list.addItem(f"New Source SkinCluster {count + 1}")

    def load_target_skin_clusters(self):
        """
        Load target skin clusters into the list widget.
        """
        count = self.target_source.source_list.count()
        self.target_source.source_list.addItem(f"New Target SkinCluster {count + 1}")

    def remove_selected_skin_cluster(self):
        """
        Remove selected skin clusters from the list widget.
        """
        source_selected_items = self.load_source.source_list.selectedItems()
        target_selected_items = self.target_source.source_list.selectedItems()
        if source_selected_items:
            for item in source_selected_items:
                row = self.load_source.source_list.row(item)
                self.load_source.source_list.takeItem(row)
        if target_selected_items:
            for item in target_selected_items:
                row = self.target_source.source_list.row(item)
                self.target_source.source_list.takeItem(row)
        if not source_selected_items and not target_selected_items: 
            print("No skin clusters selected.")

    def move_source_to_target(self):    
        """
        Move selected source skin clusters to the target list widget.       
        """ 
        source_selected_items = self.load_source.source_list.selectedItems()
        if source_selected_items:
            for item in source_selected_items:
                row = self.load_source.source_list.row(item)
                target_item = self.load_source.source_list.takeItem(row)
                self.target_source.source_list.addItem(target_item)
        else:
            print("No source skin clusters selected.")

    def move_target_to_source(self):   
        """
        Move selected target skin clusters to the source list widget.
        """ 
        target_selected_items = self.target_source.source_list.selectedItems()
        if target_selected_items:
            for item in target_selected_items:
                row = self.target_source.source_list.row(item)
                source_item = self.target_source.source_list.takeItem(row)
                self.load_source.source_list.addItem(source_item)
        else:
            print("No target skin clusters selected.")

    def combine_skin_cluster(self):
        """
        Combine selected skin clusters from the target list widget.
        """ 
        target_items = [self.target_source.source_list.item(i).text() for i in range(self.target_source.source_list.count())]
        selected_radio = "New Mesh" if self.new_mesh_radio.isChecked() else "Target Mesh"
        if target_items:
            print(f"Combined on {selected_radio}:", target_items)
        else:
            print("No target skin clusters.")


    def rebuild_skin_cluster(self): 
        """ 
        Rebuild selected skin clusters from the source and target list widgets.
        """

        source_selected_items = [self.load_source.source_list.item(i).text() for i in range(self.load_source.source_list.count())]
        target_selected_items = [self.target_source.source_list.item(i).text() for i in range(self.target_source.source_list.count())]
        selected_radio = "New Mesh" if self.new_mesh_radio.isChecked() else "Target Mesh"
        if source_selected_items or target_selected_items:
            print(f"Rebuilt on {selected_radio}:", source_selected_items + target_selected_items)
        else:
            print("No skin clusters to rebuild.")

    def apply_stylesheet(self):
        """
        Apply the stylesheet to the UI.
        """
        stylesheet = self.load_stylesheet_from_json(self.json_path)
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def load_stylesheet_from_json(self, json_path):
        """
        Load the stylesheet from a JSON file.   
        Args:
            json_path (str): The path to the JSON file containing the stylesheet.
        Returns:
            str: The loaded stylesheet as a string.
        """
        if not os.path.exists(json_path):
            print(f"Stylesheet not found: {json_path}")
            return None

        try:
            with open(json_path, "r") as file:
                style_dict = json.load(file)

            style_sheet = ""
            for selector, props in style_dict.items():
                style_sheet += f"{selector} {{\n"
                for prop, val in props.items():
                    style_sheet += f"    {prop}: {val};\n"
                style_sheet += "}\n"
            return style_sheet
        except Exception as e:
            print(f"Failed to load stylesheet: {e}")
            return None




