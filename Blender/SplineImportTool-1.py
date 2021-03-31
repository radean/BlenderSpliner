bl_info = {
    "name": "SplineImport",
    "author": "radean",
    "version": (1, 4),
    "blender": (2, 80, 0),
    "location": "import-export",
    "description": "Import spline from UE4's B2Spline using CSV notation Method",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

import bpy, csv
# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
import collections
from mathutils import Euler, Matrix, Quaternion, Vector
from bpy import context, data, ops
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


# store keymaps here to access after registration
addon_keymaps = []
NormalizeFactor = .01
Is_selected = False

#Definig Definitions
def makehash():
    return collections.defaultdict(makehash)

# Array Cleaner
def PSort(i, a):
    b = a[i] * NormalizeFactor
    return float(b)

#Spline Detail Arrays
SplinesPointsPosition = []
SplinesInTangent = []
SplinesOutTangent = []

SplinePoints = []


SplinePoint = {
    'Px' : [],
    'Py' : [],
    'Pz' : [],
    'iTx' : [],
    'iTy' : [],
    'iTz' : [],
    'oTx' : [],
    'oTy' : [],
    'oTz' : []
}

#    "position": {"X", "Y", "Z"},
#    "inTangent": {"X", "Y", "Z"},
#    "outTangent": {"X", "Y", "Z"}


#SplinePoint = makehash()
# User-Interaction Warning Dialog
def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)



# Reading CSV file and biulding points
def read_some_data(context, filepath, use_some_setting):
    # incremental Counter
    counter = 0;
    counterInt = 0;
    counterParam = 0;
    
    # Closeup all the content Cache
    SplinesPointsPosition.clear() 
    SplinesInTangent.clear() 
    SplinesOutTangent.clear() 
    SplinePoints.clear()
    SplinePoint = {
        'Px' : [],
        'Py' : [],
        'Pz' : [],
        'iTx' : [],
        'iTy' : [],
        'iTz' : [],
        'oTx' : [],
        'oTy' : [],
        'oTz' : []
    }
    
    print("Before Application", SplinePoint)
    
    print("Importing the CSV and building spline points")
    #Opening File in Memory
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        fileN = filepath
        results = list(csv.reader(csvfile))
        for i, row in enumerate( results ):
            if i == 0: continue
            counter+=1
            SplinesPointsPosition.append(row[1])
            SplinesInTangent.append(row[2])
            SplinesOutTangent.append(row[3])
#            print("Points Counter", counter)
    
    
    spline = bpy.ops.curve.primitive_bezier_curve_add(
                                            radius=100, 
                                            enter_editmode=True, 
                                            location=(0, 0, 0))

    # Subdivide the curve by a number of cuts, giving the
    # random vertex function more points to work with.
    
    
    counterParam = counter / 1000;
    counterParam = round(counterParam) - 1
    print("Max Definition: ",counter ,round(counterParam))
    ops.curve.subdivide(number_cuts=counter-2)
    
    if (counterParam <= 1):
        pass;
    elif (counterParam != 0):
        ops.curve.subdivide(number_cuts=counterParam)
        
    
    
    #Setting it to Poly
    # spline.spline_type_set(type='POLY')
    
    
#    Patching the Pointers
    for i in SplinesPointsPosition:
        if i == 0: continue
        #Removing First and Last Index
        i = i[1:-1]
        #Stripping not-required indeces
        i = i.split(",")
        #print ("OutTangent info  X =   ", i[0][2:])
        x = [float(i) for i in [i[0][2:]]]
        y = [float(i) for i in [i[1][2:]]]
        z = [float(i) for i in [i[2][2:]]]
#        format = Vector(x, y, z)
        SplinePoint['Px'].extend(x)
        SplinePoint['Py'].extend(y)
        SplinePoint['Pz'].extend(z)
    
    
#    Patching the Tanget IN Pointers
    for i in SplinesInTangent:
        if i == 0: continue
        #Removing First and Last Index
        i = i[1:-1]
        #Stripping not-required indeces
        i = i.split(",")
        #print ("OutTangent info  X =   ", i[0][2:])
        x = [float(i) for i in [i[0][2:]]]
        y = [float(i) for i in [i[1][2:]]]
        z = [float(i) for i in [i[2][2:]]]
#        format = Vector(x, y, z)
        SplinePoint['iTx'].extend(x)
        SplinePoint['iTy'].extend(y)
        SplinePoint['iTz'].extend(z)
        
#    Patching the Tanget Out Pointers
    for i in SplinesOutTangent:
        if i == 0: continue
        #Removing First and Last Index
        i = i[1:-1]
        #Stripping not-required indeces
        i = i.split(",")
        #print ("OutTangent info  X =   ", i[0][2:])
        x = [float(i) for i in [i[0][2:]]]
        y = [float(i) for i in [i[1][2:]]]
        z = [float(i) for i in [i[2][2:]]]
#        format = Vector(x, y, z)
        SplinePoint['oTx'].extend(x)
        SplinePoint['oTy'].extend(y)
        SplinePoint['oTz'].extend(z)
    
    
    #Getting the Spline from the Scene
    curve = context.active_object
    #Getting the spline points
    bzs = curve.data.splines[0].bezier_points
    
#    print(bpy.Type(bzs))
    bzspline = list(curve.data.splines[0].bezier_points)
    print("Total Enumerae storage", len(bzspline))
    
    
    # Setting the points positions
#    for ( i = 0; i < counter.length; i++):
#        print(bz)
    for i, bz in enumerate(bzspline):
        #Break if the count is more than the counter of the rows in CSVs
        
    
        if (i==counter+1):
            print("COPPA")
            break;
        
        counterInt = counterInt + 1
        
        #elif (i==counter-1):
            #continue;
#       Creating a Vector3 using maths Utilities
        position = Vector((PSort(i, SplinePoint['Px']), PSort(i, SplinePoint['Py']), PSort(i, SplinePoint['Pz'])))
        inTangent = Vector((PSort(i, SplinePoint['iTx']), PSort(i, SplinePoint['iTy']), PSort(i, SplinePoint['iTz'])))
        outTangent = Vector((PSort(i, SplinePoint['oTx']), PSort(i, SplinePoint['oTy']), PSort(i, SplinePoint['oTz'])))
#        print("Position", position)
#        print("inTangent", inTangent)
#        print("outTangent", outTangent)
        bz.co = position
        bz.handle_left = outTangent
        bz.handle_right = inTangent
#        
    
    print("Total Iteration for BZS", counterInt)
    bzs = None
    spline = None
    
    #print(bz[0].co)
    
    # Return to object mode.
    ops.object.mode_set(mode='OBJECT')
    #curve.name = fileN
    # Closeup all the content Cache
    SplinesPointsPosition.clear() 
    SplinesInTangent.clear() 
    SplinesOutTangent.clear() 
    SplinePoints.clear()
    
    # Finishing the function Here
    return {'FINISHED'}


#Import Spline CSV
class ImportSplineCSV(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.spline_i"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import CSV Data"
    


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
        name="From GPXConverter(Whoosh)",
        description="EXPERIMENTAL -- Us eto greatly increase the chances of getting spline moved to engine without sacrificing much of it details and commercing the line aboves",
        default=False,
    )
 
    def execute(self, context):
        return read_some_data(context, self.filepath, self.use_setting)

# Only needed if you want to add into a dynamic menu

#Spline import data fetcher
def menu_func_import(self, context):
    self.layout.operator(ImportSplineCSV.bl_idname, text="Import Spline CSV")

def register():
    bpy.utils.register_class(ImportSplineCSV)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    kmi = km.keymap_items.new(ImportSplineCSV.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
#    kmi.properties.total = 4

    addon_keymaps.append(km)



def unregister():
    bpy.utils.unregister_class(ImportSplineCSV)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_export)


if __name__ == "__main__":
    register()
    
    bpy.ops.import_test.spline_i('INVOKE_DEFAULT')
    # test call
#    if bpy.context.selected_objects[0].type != 'CURVE':
#        ShowMessageBox("Please select a valid Spline for replacing points according to the CSV", "Not a Spline", 'ERROR')
#    elif bpy.context.selected_objects[0].type == 'CURVE': 
#        bpy.ops.import_test.spline_io('INVOKE_DEFAULT')
#    elif bpy.context.selected_objects.length == 0:
#        ShowMessageBox("Nothing is selected", "Not a Spline", 'ERROR')
        
#    elif bpy.context.scene.objects.active:
#        ShowMessageBox("Please select a valid Spline for saving bezier Coordinates", "Nothing is selected, or selected in wrong mode", 'INFO')
    
#bpy.context.scene.objects.active == 'NONE':