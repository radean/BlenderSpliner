bl_info = {
    "name": "SplineMetaTools",
    "author": "Vishal Baba Yaga",
    "version": (0, 0, 1),
    "description": "Major Development tool for the Spline Communication and multiple spline development",
    "blender": (2, 90, 0),
    "category": "Utility",
}

import bpy
import random
import json

addon_keymaps = []
warerr_emptySelection = [
"Nothing is Selected, Please First Select the object(s)",
"Please First Select Something",
"Kindly Select Something"
]

# Generic Meta Class for the Generic Operators
class GenericOperator(bpy.types.Operator):
    global selectedObject
    selectedObject = bpy.context.selected_objects
    
#    global selectedObjectdata
#    selectedObjectdata = bpy.data.selected_objects
    
    # Results
    global result
    result = []
    
    def execute(self, context):
        self.initializeSequece()
        return {'FINISHED'}
    
# Additional Scripted Menu
class baseMenus(bpy.types.Menu):
    bl_label = "Base-Spline"
    bl_idname = "baseMenus"
    
    def draw(self, context):
        layout = self.layout
    
        layout.operator("wm.splinify", text=" Apply Splinify")
        

class customMenu(bpy.types.Menu):
    bl_label = "Multi-Spline"
    bl_idname = "customMenu"
    
    def draw(self, context):
        layout = self.layout
        
        # call another menu
        # Test Button Template to copy and use
        # layout.operator("wm.call_menu", text="Unwrap", icon="MESH_DATA").name = "VIEW3D_MT_uv_map"
        
        # Add Splinify Button
        # Adding customized parameters for the spline generic generation processes
        # To Define a Splinify Object Generally a Trigger Box, Ready for the UE 4 Multiple spline Feature
        layout.operator("wm.splinify", text=" Apply Splinify")
        
        # Removing Splinify Button
        # Removing any additional Custome parameters inside the object (Trigger Box)
        # To UnDefine the spline Friendly Trigger Box
        layout.operator("wm.removesplinify", text=" Remove Splinify")
        
        # Removing Splinify Button
        # Removing any additional Custome parameters inside the object (Trigger Box)
        # To UnDefine the spline Friendly Trigger Box
        layout.operator("wm.exporttriggerboxes", text=" Export Trigger Box")
        
        #Getting the custom Property ranges
        #grab = bpy.context.selected_objects[0]["Sectional"]
        
        #Calling intexs methods
        #customMenu.grewPrint(grab)
    
# Make Spline Meta
class Splinify(GenericOperator):
    bl_idname = "wm.splinify"
    bl_label = "Add Splinify"
    bl_description = "Add Custom Properties and scripts to the selected Trigger Box(s)"
    
#    # Setting a Base Actor
#    global customProps
#    customProps = bpy.context.selected_objects

    def execute(self, context):
        Splinify.initializeSequece()
        return {'FINISHED'}
    
    def initializeSequece():
        # Checking if object is selected
        if (len(selectedObject)):
            # Iterating Objects one by One
            for customProp in selectedObject:
                # Adding the following custom Properties
                customProp["ID"] = int(0)
                customProp["Name"] = str("Staple")
                customProp["PrimarySplineID"] = str("Stinger")
                customProp["PrimaryRouteID"] = int(0) # Any Integer
                customProp["PrimarySplineButtonIndex"] = int(0) # Any Integer
                customProp["PrimarySplineDirection"] = int(0) # 0 = Backward, 1 = Forward
                customProp["ShowPathSelectionDirection"] = int(0) # 0 = Backward, 1 = Forward
                customProp["SplineSwitch"] = int(0) # 0 = Normal, 1 = With Deadend, 2 , 3 
#                customProp["ConnectedSplineA"] = str("Not Assigned") # Curve Name
#                customProp["ConnectedSplineB"] = str("Not Assigned") # Curve Name
        else:
            print("Nothing is Selected")
            
            
            
class RemoveSplinify(GenericOperator):
    bl_idname = "wm.removesplinify"
    bl_label = "Remove Splinify"
    bl_description = "Remove all the Custom Properties and scripts of the selected Trigger Box(s)"

    def execute(self, context):
        RemoveSplinify.initializeSequece()
        return {'FINISHED'}
    
    def initializeSequece():
        if (len(selectedObject)):
            for customProp in selectedObject:
                if (len(customProp.keys())):
                    del customProp["ID"]
                    del customProp["Name"]
                    del customProp["PrimarySplineID"]
                    del customProp["PrimaryRouteID"]
                    del customProp["PrimarySplineButtonIndex"]
                    del customProp["PrimarySplineDirection"]
                    del customProp["ShowPathSelectionDirection"]
                    del customProp["SplineSwitch"]
#                    del customProp["ConnectedSplineA"]
#                    del customProp["ConnectedSplineB"]
        else:
            print(warerr_emptySelection[random.randint(0, len(warerr_emptySelection) - 1)])


# Get All selected TriggerBox Data
#
#
#

class ExportTriggerBoxes(GenericOperator):
    bl_idname = "wm.exporttriggerboxes"
    bl_label = "Export Trigger Boxes"
    bl_description = "Remove all the Custom Properties and scripts of the selected Trigger Box(s)"

    def execute(self, context):
        ExportTriggerBoxes.initializeSequece()
        return {'FINISHED'}
    
    def initializeSequece():
        
        # Check if some objects is Selected
        if (len(selectedObject)):
            #result = []
            spline_track = []
            #spline_track["data"] = []
            # Iterate the Trigger Boxes in the Scene
            for triggerBox in selectedObject:
                # For each trigger bos 
                spline_dict = {}
                spline_dict["Name"] = triggerBox.name
                spline_dict["Position"] = {}
                spline_dict["Rotation"] = {}
                spline_dict["Scale"] = {}
                spline_dict["CProperties"] = {}
                
                spline_dict["Position"]["x"] = triggerBox.location[0]
                spline_dict["Position"]["y"] = triggerBox.location[1]
                spline_dict["Position"]["z"] = triggerBox.location[2]
                
                spline_dict["Rotation"]["x"] = triggerBox.rotation_euler[0]
                spline_dict["Rotation"]["y"] = triggerBox.rotation_euler[1]
                spline_dict["Rotation"]["z"] = triggerBox.rotation_euler[2]
                
                spline_dict["Scale"]["x"] = triggerBox.scale[0]
                spline_dict["Scale"]["y"] = triggerBox.scale[1]
                spline_dict["Scale"]["z"] = triggerBox.scale[2]
                
                # Fetching all the custom properties values
                for customProperty in triggerBox.keys():
                    
                    # Assigning each value into the Json Dumper 
                    spline_dict["CProperties"][customProperty] = str(triggerBox[customProperty])
                
                
                # Appending the collected data
                #spline_track["data"].append(spline_dict)
                spline_track.append(spline_dict)
                
                
            result.append(spline_track)
            
            #print("Copied List", result)
            
            ## Invoking the exporter UI
            bpy.ops.triggerboxes.export_json('INVOKE_DEFAULT')
        else:
            print(warerr_emptySelection[random.randint(0, len(warerr_emptySelection) - 1)])



# Defining the json methods to write the transforms and other information of all cube
#
def write_json_data(context, filepath,json_data):
    with open(filepath, 'w', encoding='utf-8') as f:
        print(json.dump(json_data, f, ensure_ascii=False, indent=4))
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        
    f.close()
    return {'FINISHED'}

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportDataPatch(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "triggerboxes.export_json"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Trigger Box Data to Json"
    
    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    def execute(self, context):
        points = result
        return write_json_data(context, self.filepath, points)

#def grewPrint():
#    print("BaseClose") 
def draw_item(self, context):
    layout = self.layout
    layout.menu(customMenu.bl_idname)

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportDataPatch.bl_idname, text="GPX Export Operator")


def register():
    #Main ClassQQ
    # Initial object and addon
    bpy.utils.register_class(customMenu)
    bpy.utils.register_class(baseMenus)
    bpy.types.VIEW3D_MT_object.append(draw_item)
    
    #Operator Classes
    # Supportive classes for calling a whole class by a method
    bpy.utils.register_class(ExportTriggerBoxes)
    bpy.utils.register_class(ExportDataPatch)
    bpy.utils.register_class(Splinify)
    bpy.utils.register_class(RemoveSplinify)
    

    # lets add ourselves to the main header
    bpy.types.INFO_HT_header.append(draw_item)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', shift=True, alt=True)
    kmr = km.keymap_items.new('wm.call_menu', 'W', 'PRESS', shift=True, alt=True)
    kmi.properties.name = customMenu.bl_idname
    kmr.properties.name = baseMenus.bl_idname
    #kmi.properties.total = 4

    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(customMenu)
    
    km.keymap_items.remove(kmi)

    bpy.types.INFO_HT_header.remove(draw_item)
    
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=customMenu.bl_idname)
    #bpy.ops.triggerboxes.export_json('INVOKE_DEFAULT')

#       hope you are doing good, 
#
#
#