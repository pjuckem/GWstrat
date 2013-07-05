# Import arcpy module
import math
try:
    import arcpy
    from arcpy import env
except: 
    print ('\n'
           'ERROR: Unable to import the "ARCPY" module. \n\n'
           'The program will not work without this module. \n'
           'Please ensure that ARC9.3 or newer is installed and \n'
           'the python path includes a path to ARCPY. \n\n')
    arcpy.AddError ('\n'
               'ERROR: Unable to import the "ARCPY" module. \n\n'
               'The program will not work without this module. \n'
               'Please ensure that ARC9.3 or newer is installed and \n'
               'the python path includes a path to ARCPY. \n\n')    

try:
    env.workspace = "c:/"
except:
    print ('\n'
            'ERROR: Unable to set the workspace to C:\. \n\n'
            'The program writes temporary files, and requires \n'
            'write access to C:\. Please work with your IT\n'
            'staff to ensure you have write access to C:\. \n\n')
    arcpy.AddError ('\n'
            'ERROR: Unable to set the workspace to C:\. \n\n'
            'The program writes temporary files, and requires \n'
            'write access to C:\. Please work with your IT\n'
            'staff to ensure you have write access to C:\. \n\n')    

# Check out any necessary licenses
if arcpy.CheckExtension("spatial") == "Available":
    arcpy.CheckOutExtension("spatial")
else:
    print ('ERROR: Spatial Analyst is required for this tool, but \n'
           'the license is unavailable. Please work with your IT \n'
           'staff to ensure that your installation of ARC includes \n'
           'a license for Spatial Analyst. \n')  
    arcpy.AddError ('ERROR: Spatial Analyst is required for this tool, but \n'
           'the license is unavailable. Please work with your IT \n'
           'staff to ensure that your installation of ARC includes \n'
           'a license for Spatial Analyst. \n')      
    
env.overwriteOutput = True

# Start of main code
#arcpy.SetProgressor('step','Computing groundwater age...', 0,6,1)
#arcpy.SetProgressorLabel('Reading data entries...')
#arcpy.SetProgressorPosition()

pointfc = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\Waupaca\\ARC\\test\\fp9_test.shp"
newfieldname = "c_piston"

# specify fields for calculations
pointdesc = arcpy.ListFields(pointfc)
rows = arcpy.SearchCursor(pointfc)
Wbot = "Well_Depth"
Wscreen = "Screen_len"

for row in rows:
    for field in pointdesc:
        if (field.name == Wbot):
            z2 = row.getValue(field.name)
            print "%s: %s" % (field.name, row.getValue(field.name))
        if (field.name == Wscreen):
            z1 = z2 - row.getValue(field.name)
            print "%s: %s" % (field.name, row.getValue(field.name))


watertable = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\Waupaca\\GWstrat\\WP4_heads.GRD"
bottom = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\Waupaca\\ARC\\wp4_heads1"
porosity = 0.2
recharge = '0.87'
percentdepthstr = '63'
Output_raster_name = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\Waupaca\\GWstrat\\GWAStest2"
'''
watertable = arcpy.GetParameterAsText(0)
bottom = arcpy.GetParameterAsText(1)
porosity = arcpy.GetParameterAsText(2)
recharge = arcpy.GetParameterAsText(3)
percentdepthstr = arcpy.GetParameterAsText(4)
Output_raster_name = arcpy.GetParameterAsText(5)
'''
sat_thick = "Minus_1"
DepthRaster = "Times_1"
Output_raster__2_ = "Times_2"
MeanAgeRaster = "divide_1"
Minus_GRD2 = "Minus_2"
DratioRaster = "divide_2"
Ln_DratioRaster = "ln_grd"


'''sat_thick = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Minus_1"
DepthRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Times_1"
Output_raster__2_ = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Times_2"
MeanAgeRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\divide_1"
Minus_GRD2 = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Minus_2"
DratioRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\divide_2"
Ln_DratioRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\ln_grd"
'''

# add a field to an existing point shapefile of the wells
'''arcpy.AddField_management(wells,newfieldname,"FLOAT",5,1,"",'Calc_well_age_Piston')

# calculate the theoretical age for the well based on aquifer and well constriction properties
CalcPiston =  (Wbot-Wscreen)
arcpy.CalculateField_management(pointfc,newfieldname,CalcPiston,"PYTHON")
'''
'''
# Process: Minus
arcpy.gp.Minus_sa(watertable, bottom, sat_thick)
#arcpy.SetProgressorLabel('Computing saturated thickness...')
#arcpy.SetProgressorPosition()

# Process: Times
arcpy.gp.Times_sa(sat_thick, porosity, Output_raster__2_)
#arcpy.SetProgressorLabel('Computing groundwater ages...')
#arcpy.SetProgressorPosition()

# Process: Divide
arcpy.gp.Divide_sa(Output_raster__2_, recharge, MeanAgeRaster)
#arcpy.SetProgressorPosition()

# Compute small d
percentdepth = int(percentdepthstr) / 100.0
arcpy.gp.Times_sa(sat_thick, percentdepth, DepthRaster)
#arcpy.SetProgressorPosition()

# compute ln(D/D-d) as a constant.  This approach works when depth is specified as a
# percent of total depth, because the end result will be the same for all cells as
# can be shown with this example using 20% of saturated depth: 10 / (10 - 0.2*10) =  1.25
# The same result for 20% occurs with any value (try 200, 999, etc).

Dratio = (10.0 / (10.0 - (percentdepth * 10)))
ln_Dratio = math.log(Dratio)
arcpy.gp.Times_sa(MeanAgeRaster, ln_Dratio, Output_raster_name)
#arcpy.SetProgressorLabel('Generating the groundwater age raster...')
#arcpy.SetProgressorPosition()

arcpy.CheckInExtension("spatial")
'''