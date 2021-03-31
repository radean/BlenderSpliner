bl_info = {
    "name": "SplineExport",
    "author": "radean",
    "version": (1, 12),
    "blender": (2, 80, 0),
    "location": "import-export",
    "description": "Exports spline to UE4 using CSV notation Method",
    "warning": "",
    "wiki_url": "",
    "category": "Export",
}

import bpy
# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


# store keymaps here to access after registration
addon_keymaps = []
NormalizeFactor = 100
Is_selected = False

# Getting the object activation
#for object in bpy.context.selected_objects:
#    print(object.name)
    
print(Is_selected)


# User-Interaction Warning Dialog
def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)



# Write functional assignemnts
def write_some_data(context, filepath, use_some_setting):
    # incremental Counter
    counter = 0;
    
    
    print("Exporitng spline with points by writing the csv")
    #Opening File in Memory
    file = open(filepath, 'w', encoding='utf-8')
    
    #Writing file contents
    file.write('---,Position,InTangent,OutTangent\n');
    # Iterating into the selected object
    for ob in bpy.context.selected_objects:
        # Determining the type of the selected object
        if ob.type == 'CURVE':
            # Iterating Spline points data
            for spline in ob.data.splines:
                # Determining the length of the program
                if len(spline.bezier_points) > 0:
                    # Iterating through tht bezier points
                    for bezier_point in spline.bezier_points.values():
                        # Writing the file with beziers
                        file.write('%s,' % str(counter));
                        # Determing the position in the world
                        co = ob.matrix_world @ bezier_point.co;
                        # Determinig the handle position of point tangents
                        handle_in = ob.matrix_world @ bezier_point.handle_right;
                        handle_out = ob.matrix_world @ bezier_point.handle_left;
                        # writing the Handles data
                        file.write('"(X=%.3f,Y=%.3f,Z=%.3f)",' % (co.y * NormalizeFactor, co.x * NormalizeFactor, co.z * NormalizeFactor));
                        file.write('"(X=%.3f,Y=%.3f,Z=%.3f)",' % (handle_in.y * NormalizeFactor, handle_in.x * NormalizeFactor, handle_in.z * NormalizeFactor));
                        file.write('"(X=%.3f,Y=%.3f,Z=%.3f)"\n' % (handle_out.y * NormalizeFactor, handle_out.x * NormalizeFactor, handle_out.z * NormalizeFactor));
                        #incrementing the pointer
                        counter += 1;
            
    
    #f.write("Hello World %s" % use_some_setting)
    file.close()


    # Finishing the function Here
    return {'FINISHED'}



class ExportSplineData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.spline_e"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export CSV Data"
    

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Cryptogen Generation",
        description="EXPERIMENTAL -- Method that export the definition of legacy exporter and combination, generally depends on algorithm that forces engine to produce the best applicable to get it all done",
        default=False,
    )

    type: EnumProperty(
        name="GRM Method",
        description="Export Method",
        items=(
            ('OPT_A', "Point-Based", "Point based solver only export and move the base interface of points/vertex proximity and transform"),
            ('OPT_B', "Bezier-Based", "Bezier based solver relays the basic points and tangents figures "),
        ),
        default='OPT_A',
    )

    
    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSplineData.bl_idname, text="Spline Export Operator")


def register():
    bpy.utils.register_class(ExportSplineData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    kmi = km.keymap_items.new(ExportSplineData.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
#    kmi.properties.total = 4

    addon_keymaps.append(km)



def unregister():
    bpy.utils.unregister_class(ExportSplineData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    if bpy.context.selected_objects[0].type != 'CURVE':
        ShowMessageBox("Please select a valid Spline for saving bezier Coordinates", "Not a Spline", 'ERROR')
    elif bpy.context.selected_objects[0].type == 'CURVE': 
        bpy.ops.export_test.spline_e('INVOKE_DEFAULT')
#    elif bpy.context.selected_objects.length == 0:
#        ShowMessageBox("Nothing is selected", "Not a Spline", 'ERROR')
        
#    elif bpy.context.scene.objects.active:
#        ShowMessageBox("Please select a valid Spline for saving bezier Coordinates", "Nothing is selected, or selected in wrong mode", 'INFO')
    
#bpy.context.scene.objects.active == 'NONE':

    