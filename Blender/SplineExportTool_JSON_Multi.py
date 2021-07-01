import bpy
import json
addon_keymaps = []
NormalizeFactor = 100

def GetSplineCurveData(context):
    selected_objects = bpy.context.selected_objects
    result = []
    for ob in selected_objects:
        spline_track = {}
        spline_track["name"] = "BaseSpline" + str(selected_objects.index(ob))
        spline_track["data"] =[]
        # Determining the type of the selected object
        if ob.type == 'CURVE':
            # Iterating Spline points data
            for spline in ob.data.splines:
                # Determining the length of the program
                if len(spline.bezier_points) > 0:
                    # Iterating through tht bezier points
                    for bezier_point in spline.bezier_points.values():
                        #spline_points = []
                        spline_dict = {}
                        spline_dict["Position"] = {}
                        spline_dict["InTangent"] = {}
                        spline_dict["OutTangent"] = {}

                        # Determing the position in the world
                        co = ob.matrix_world @ bezier_point.co;
                        spline_dict["Position"]["x"] = co.y * NormalizeFactor 
                        spline_dict["Position"]["y"] = co.x * NormalizeFactor
                        spline_dict["Position"]["z"] = co.z * NormalizeFactor
                       
                        # Determinig the handle position of point tangents
                        handle_in = ob.matrix_world @ bezier_point.handle_right;
                        spline_dict["InTangent"]["x"] = handle_in.y * NormalizeFactor
                        spline_dict["InTangent"]["y"] = handle_in.x * NormalizeFactor
                        spline_dict["InTangent"]["z"] = handle_in.z * NormalizeFactor    
                         
                        handle_out = ob.matrix_world @ bezier_point.handle_left;
                        spline_dict["OutTangent"]["x"] = handle_out.y * NormalizeFactor
                        spline_dict["OutTangent"]["y"] = handle_out.x * NormalizeFactor
                        spline_dict["OutTangent"]["z"] = handle_out.z * NormalizeFactor   

                        #spline_points.append(spline_dict)
                        spline_track["data"].append(spline_dict)
        result.append(spline_track)
    return result               

def write_json_data(context, filepath,json_data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportGPXData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "spline_curve.export_json"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Curve Data to Json"

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )


    def execute(self, context):
        points = GetSplineCurveData(context)
        return write_json_data(context, self.filepath,points)

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportGPXData.bl_idname, text="GPX Export Operator")


def register():
    bpy.utils.register_class(ExportGPXData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportGPXData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.spline_curve.export_json('INVOKE_DEFAULT')
