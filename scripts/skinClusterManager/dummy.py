import json
import os

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui


class SkinClusterManager(QtWidgets.QDialog):
    def __init__(self):
        super(SkinClusterManager, self).__init__(wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow))
        self.setWindowTitle("SkinCluster Manager")
        self.setMinimumSize(300, 400)

        self.json_path = os.path.join(os.path.dirname(__file__), "styleSheet.json")

        self.svg_path = os.path.join(os.path.dirname(__file__), "images.json")

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.apply_stylesheet()

    def create_widgets(self):
        self.load_source_btn = QtWidgets.QPushButton("Load Source")
        self.source_list = QtWidgets.QTreeWidget()
        self.source_list.setHeaderHidden(True)

        # Create top-level items
        spine_item = QtWidgets.QTreeWidgetItem(self.source_list, ["Spine"])
        arm_item = QtWidgets.QTreeWidgetItem(self.source_list, ["Arm"])
        face_item = QtWidgets.QTreeWidgetItem(self.source_list, ["Face"])
        leg_item = QtWidgets.QTreeWidgetItem(self.source_list, ["Leg"])

        # Add child items to "Arm"
        hand_item = QtWidgets.QTreeWidgetItem(arm_item, ["Hand"])

        # Expand all items by default
        self.source_list.expandAll()

        self.right_btn = QtWidgets.QPushButton()
        arrow_icon = self.get_svg("arrow_forward")
        self.right_btn.setIcon(arrow_icon)
        self.left_btn = QtWidgets.QPushButton()
        arrow_icon = self.get_svg("arrow_back")
        self.left_btn.setIcon(arrow_icon)


        self.load_target_btn = QtWidgets.QPushButton("Load Target")
        self.target_list = QtWidgets.QTreeWidget()

        self.remove_skc = QtWidgets.QPushButton("Remove SkinCluster")
        self.new_mesh_radio = QtWidgets.QRadioButton()
        self.new_mesh_radio.setText("Shit Mesh")
        self.target_mesh_radio = QtWidgets.QRadioButton()
        self.target_mesh_radio.setText("Target Mesh")
        self.target_mesh_radio.setChecked(True)
        self.combine_skc = QtWidgets.QPushButton("Combine SkinCluster")
        self.rebuild_skc = QtWidgets.QPushButton("Rebuild SkinCluster")

        # -- TOOLTIPS -- #
        
        self.load_source_btn.setToolTip = "Load source skin clusters"
        self.right_btn.setToolTip = "Move selected source skin clusters to target"
        self.left_btn.setToolTip = "Move selected target skin clusters to source"
        self.load_target_btn.setToolTip = "Load target skin clusters"
        self.remove_skc.setToolTip = "Remove selected skin clusters"
        self.combine_skc.setToolTip = "Combine target skin clusters" 
        self.rebuild_skc.setToolTip = "Rebuild selected skin clusters"


    def create_layout(self):
        left_top_v_layout = QtWidgets.QVBoxLayout() 
        left_top_v_layout.addWidget(self.load_source_btn)   
        left_top_v_layout.addWidget(self.source_list)   

        middle_top_v_layout = QtWidgets.QVBoxLayout()
        middle_top_v_layout.addStretch()
        middle_top_v_layout.addWidget(self.right_btn)
        middle_top_v_layout.addWidget(self.left_btn)    
        middle_top_v_layout.addStretch()

        right_top_v_layout = QtWidgets.QVBoxLayout()
        right_top_v_layout.addWidget(self.load_target_btn)
        right_top_v_layout.addWidget(self.target_list)

        top_horizontal_layout = QtWidgets.QHBoxLayout()
        top_horizontal_layout.addLayout(left_top_v_layout)
        top_horizontal_layout.addLayout(middle_top_v_layout)    
        top_horizontal_layout.addLayout(right_top_v_layout)

        bottom_horizontal_layout = QtWidgets.QHBoxLayout()
        bottom_horizontal_layout.addWidget(self.remove_skc)
        bottom_horizontal_layout.addStretch()
        bottom_horizontal_layout.addWidget(self.new_mesh_radio)
        bottom_horizontal_layout.addWidget(self.target_mesh_radio)
        bottom_horizontal_layout.addStretch()
        bottom_horizontal_layout.addWidget(self.combine_skc)
        bottom_horizontal_layout.addWidget(self.rebuild_skc)    
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_horizontal_layout)
        main_layout.addLayout(bottom_horizontal_layout)

    def create_connections(self):
        self.load_source_btn.clicked.connect(self.load_source_skin_clusters) 
        self.load_target_btn.clicked.connect(self.load_target_skin_clusters)
        self.remove_skc.clicked.connect(self.remove_selected_skin_cluster)
        self.right_btn.clicked.connect(self.move_source_to_target)  
        self.left_btn.clicked.connect(self.move_target_to_source)
        self.combine_skc.clicked.connect(self.combine_skin_cluster)
        self.rebuild_skc.clicked.connect(self.rebuild_skin_cluster)

    def get_svg(self, name=None):
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

    def load_source_skin_clusters(self):
        count = self.source_list.count()
        self.source_list.addItem(f"New Source SkinCluster {count + 1}")

    def load_target_skin_clusters(self):
        count = self.target_list.count()
        self.target_list.addItem(f"New Target SkinCluster {count + 1}")

    def remove_selected_skin_cluster(self):
        source_selected_items = self.source_list.selectedItems()
        target_selected_items = self.target_list.selectedItems()
        if source_selected_items:
            for item in source_selected_items:
                row = self.source_list.row(item)
                self.source_list.takeItem(row)
        if target_selected_items:
            for item in target_selected_items:
                row = self.target_list.row(item)
                self.target_list.takeItem(row)
        if not source_selected_items and not target_selected_items: 
            print("No skin clusters selected.")

    def move_source_to_target(self):    
        source_selected_items = self.source_list.selectedItems()
        if source_selected_items:
            for item in source_selected_items:
                row = self.source_list.row(item)
                target_item = self.source_list.takeItem(row)
                self.target_list.addItem(target_item)
        else:
            print("No source skin clusters selected.")

    def move_target_to_source(self):    
        target_selected_items = self.target_list.selectedItems()
        if target_selected_items:
            for item in target_selected_items:
                row = self.target_list.row(item)
                source_item = self.target_list.takeItem(row)
                self.source_list.addItem(source_item)
        else:
            print("No target skin clusters selected.")

    def combine_skin_cluster(self):
        target_items = [self.target_list.item(i).text() for i in range(self.target_list.count())]
        selected_radio = "New Mesh" if self.new_mesh_radio.isChecked() else "Target Mesh"
        if target_items:
            print(f"Combined on {selected_radio}:", target_items)
        else:
            print("No target skin clusters.")

    def rebuild_skin_cluster(self): 
        source_selected_items = [self.source_list.item(i).text() for i in range(self.source_list.count())]
        target_selected_items = [self.target_list.item(i).text() for i in range(self.target_list.count())]
        selected_radio = "New Mesh" if self.new_mesh_radio.isChecked() else "Target Mesh"
        if source_selected_items or target_selected_items:
            print(f"Rebuilt on {selected_radio}:", source_selected_items + target_selected_items)
        else:
            print("No skin clusters to rebuild.")

    def apply_stylesheet(self):
        stylesheet = self.load_stylesheet_from_json(self.json_path)
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def load_stylesheet_from_json(self, json_path):
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


def show_skin_cluster_manager():

    try:
        ui.close()
    except:
        pass

    ui = SkinClusterManager()
    ui.show()