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

wellfile = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\GWstrat\\LUSag2_test3.shp"
fields = arcpy.ListFields(wellfile)
for field in fields:
    if str(field.name) == "WELL_DEPTH":
        depthwell = str(field.name)
    if str(field.name) == "DEPTH_TOP_":
        casingdepth = field.name
    if str(field.name) == "ALTITUDE":
        alt = field.name
    if str(field.name) == "DTW_meas":
        dtw = str(field.name)
    if str(field.name) == "SampleAge":
        sampleage = str(field.name)        
watertable = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\Waupaca\\UWSP data\\CCMF\\L1head_ft"
bottom = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\Waupaca\\UWSP data\\CCMF\\l1bot_ft"
n = 0.2
R = 0.9 #ft/yr, derived from 11.4 in/yr as per DASAAD
#Output_raster_name = "D:\\PFJData2\\Projects\\NAQWA\\Cycle3\\Waupaca\\GWstrat\\GWAStest1"

# read input files
'''
wellfile = arcpy.GetParameterAsText(0)  # point shapefile with well data
depthwell = arcpy.GetParameterAsText(1) # field in shapefile's table
casingdepth = arcpy.GetParameterAsText(2) # field in shapefile's table
alt = arcpy.GetParameterAsText(3) # field in shapefile's table
dtw = arcpy.GetParameterAsText(4) # field in shapefile's table
#topo = arcpy.GetParameterAsText(3)
watertable = arcpy.GetParameterAsText(5) # raster of water table elevation
bottom = arcpy.GetParameterAsText(6) # raster of base elevation
n = arcpy.GetParameterAsText(7) # float value of porosity
R = arcpy.GetParameterAsText(8) # float value of recharge
#Output_raster_name = arcpy.GetParameterAsText(8)
'''
# assign names to raster files that will be created

#sat_thick = "minus_1"

'''sat_thick = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Minus_1"
DepthRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Times_1"
Output_raster__2_ = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Times_2"
MeanAgeRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\divide_1"
Minus_GRD2 = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\Minus_2"
DratioRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\divide_2"
Ln_DratioRaster = "C:\\Users\\pfjuckem\\Documents\\ArcGIS\\Default.gdb\\ln_grd"
'''

# Generate saturated thickness raster
#arcpy.gp.Minus_sa(watertable, bottom, sat_thick)

# ######################################################
# Compute theoretical GW age for wells in a shapefile  #
# using the parital exponential model from TracerLPM   #
# ######################################################
try:
    # Process: Extract Values to Points
    arcpy.gp.ExtractMultiValuesToPoints_sa(wellfile, [[watertable, "WT_Rast"], [bottom,"BaseRast"]], "NONE")   #extract values from DEMs & append to point shapefile attributes
    
    #add fields to point shapefile
    #arcpy.AddField_management(wellfile, "DTW_calc", "FLOAT", "", "", "", "Depth_to_Watertable_from_rasters", "", "", "")
    #arcpy.AddField_management(wellfile, "DTBot", "FLOAT", "", "", "", "Depth_to_Bottom_from_rasters", "", "", "")
    arcpy.AddField_management(wellfile, "Z1_pts", "FLOAT", "", "", "", "Depth_to_top_of_screen_from_water_table_from_reported_DTW", "", "", "") #
    arcpy.AddField_management(wellfile, "Z2_pts", "FLOAT", "", "", "", "Depth_to_bottom_of_screen_from_water_table_from_reported_DTW", "", "", "")
    arcpy.AddField_management(wellfile, "H_pts", "FLOAT", "", "", "", "Calc_Saturated_thickness_(H)_from_MeasDTW_&_BaseRaster", "", "", "")
    arcpy.AddField_management(wellfile, "AGE_pts", "FLOAT", "", "", "", "Calc_age_from_Z1,Z2,H_pts", "", "", "")
    arcpy.AddField_management(wellfile, "Z1_rast", "FLOAT", "", "", "", "Depth_to_top_of_screen_from_water_table_raster", "", "", "") #
    arcpy.AddField_management(wellfile, "Z2_rast", "FLOAT", "", "", "", "Depth_to_bottom_of_screen_from_water_table_raster", "", "", "") #
    arcpy.AddField_management(wellfile, "H_rast", "FLOAT", "", "", "", "Calc_Saturated_thickness_(H)_from_rasters", "", "", "")
    arcpy.AddField_management(wellfile, "AGE_rast", "FLOAT", "", "", "", "Calc_age_from_Z1,Z2,H_rast", "", "", "")
    arcpy.AddField_management(wellfile, "Pt_er", "FLOAT", "", "", "", "Residual_for_age_from_H-pts", "", "", "")
    arcpy.AddField_management(wellfile, "Rst_er", "FLOAT", "", "", "", "Residual_for_age_from_H-rast", "", "", "")
    
    #calculate values for new fields

    #arcpy.CalculateField_management(wellfile, "Z1_pts", "casingdepth - !dtw!", "PYTHON_9.3")
    #arcpy.CalculateField_management(wellfile, "Z2_pts", "depthwell - dtw", "PYTHON_9.3")
    #arcpy.CalculateField_management(wellfile, "H_pts", "(alt - dtw) - bottom", "PYTHON_9.3")
    #arcpy.CalculateField_management(wellfile, "Z1_rast", "watertable - (alt - casingdepth)", "PYTHON_9.3")
    #arcpy.CalculateField_management(wellfile, "Z2_rast", "watertable - (alt - depthwell)", "PYTHON_9.3")
    #arcpy.CalculateField_management(wellfile, "H_rast", "watertable - bottom", "PYTHON_9.3")
    

    arcpy.CalculateField_management(wellfile, "Z1_pts", '!DEPTH_TOP_! - !DTW_meas!', "PYTHON_9.3")    
    arcpy.CalculateField_management(wellfile, "Z2_pts", '!WELL_DEPTH! - !DTW_meas!', "PYTHON_9.3")
    arcpy.CalculateField_management(wellfile, "H_pts", '(!ALTITUDE! - !DTW_meas!) - !BaseRast!', "PYTHON_9.3")
    arcpy.CalculateField_management(wellfile, "Z1_rast", '!WT_Rast! - (!ALTITUDE! - !DEPTH_TOP_!)', "PYTHON_9.3")
    arcpy.CalculateField_management(wellfile, "Z2_rast", '!WT_Rast! - (!ALTITUDE! - !WELL_DEPTH!)', "PYTHON_9.3")
    arcpy.CalculateField_management(wellfile, "H_rast", '!WT_Rast! - !BaseRast!', "PYTHON_9.3")    
    
except Exception as e:
    # If an error occurred, print line number and error message
    import traceback
    import sys
    tb = sys.exc_info()[2]
    print("Line {0}".format(tb.tb_lineno))
    print(e.message)


#add field for SatThick from computed and meas DTW

# Do some basic checking for inconsistancies using cursors (well by well)
wells = arcpy.UpdateCursor(wellfile)
#fields = arcpy.ListFields(wellfile)
for well in wells:  # need to edit these to loop through individual records of the fields b/c don't want to apply these to every record in the field.
    #for field in fields:
    SA = well.getValue(sampleage)
    elev = well.getValue(alt)
    depth = well.getValue(depthwell)
    bot = well.getValue("BaseRast")
    dtwater = well.getValue(dtw)
    casing = well.getValue(casingdepth)
    wt = well.getValue("WT_Rast")
    Z1_pt = well.getValue("Z1_pts")
    Z1_ras = well.getValue("Z1_rast")
    Z2_pt = well.getValue("Z2_pts")
    Z2_ras = well.getValue("Z2_rast")    
    
    # Check to see if well bottom is computed to be below the aquifer base
    wellbot = elev - depth #alt and well depth are from point file
    if wellbot < bot: # bottom is from raster
        er = bot - wellbot
        print ("The specified well bottom is %3d feet below the estimated aquifer bottom. \n"
               "The computed saturated thickness has not been adjusted, but should be improved \n"
               "prior to running the GWstrat tool with this dataset. \n" % er)
      
    #   Check to see if the watertable from measured DTW is within the screen interval. Set Z1 to zero if it is.
    if Z1_pt < 0.0: 
        er = dtwater - casing # both from point file
        Z1_pt = 0.0
        well.Z1_pts = Z1_pt
        wells.updateRow(well)
        print ("The specified top of screen for the well is %3d feet above the reported water table in the point shapefile. \n"
               "For the purposes of these calculations, the top of the screen has been reset to equal the top of the water table. \n" % er)        

    #   Check to see if the watertable (from raster) is within the screen interval. Set Z1 to zero if it is.
    screentopelev = elev - casing #alt and well casing are from point file
    if screentopelev > wt: # watertable is from raster
        er = screentopelev - wt
        Z1_ras = 0.0
        well.Z1_rast = Z1_ras
        wells.updateRow(well)        
        print ("The specified top of screen for the well is %3d feet above the estimated water table from the raster. \n"
               "For the purposes of these calculations, the top of the screen has been reset to equal the top of the water table. \n" % er)
        
    #   Check to see if the well bottom is above the watertable (from measured DTW) too. Set Z2 to 0.0001 to avoid divide-by-zero error.
    if Z2_pt < 0.0: 
        er = dtwater - depth # both from point file
        Z2_pt = 0.0001
        well.Z2_pts = Z2_pt
        wells.updateRow(well)
        print ("The specified bottom of screen for the well is %3d feet above the reported water table in the point shapefile. \n"
               "This is probably an error in the input data for the well. \n"               
               "For the purposes of these calculations, the bottom of the screen has been reset the water table, which will cause an age of zero. \n" % er)        

    #   Check to see if the well bottom is above the watertable (from raster) too. Set Z2 to 0.0001 to avoid divide-by-zero error.
    screenbotelev = elev - depth #alt and well casing are from point file
    if screenbotelev > wt: # watertable is from raster
        er = screenbotelev - wt
        Z2_ras = 0.0001
        well.Z2_rast = Z2_ras
        wells.updateRow(well)        
        print ("The specified bottom of screen for the well is %3d feet above the estimated water table from the raster. \n"
               "For the purposes of these calculations, the bottom of the screen has been set to the water table, producing an age of zero. \n" % er)
                

'''
arcpy.CalculateField_management(wellfile, AGE_pts, pts_expression, "PYTHON_9.3", pts_code)
arcpy.CalculateField_management(wellfile, AGE_rast, calc_rast_age(wellfile), "PYTHON_9.3")

pts_expression = "calc_pts_age(wellfile)"
pts_code = "def calc_pts_age(pointfile):
   "

'''
wells = arcpy.UpdateCursor(wellfile)
#fields = arcpy.ListFields(wellfile)
for well in wells:  # need to edit these to loop through individual records of the fields b/c don't want to apply these to every record in the field.
    #for field in fields:
    SA = well.getValue(sampleage)
    Z1_pt = well.getValue("Z1_pts")
    Z1_ras = well.getValue("Z1_rast")
    H_pt = well.getValue("H_pts")
    H_ras = well.getValue("H_rast")
    Z2_pt = well.getValue("Z2_pts")
    Z2_ras = well.getValue("Z2_rast")
    
    TauAq_pt = H_pt * n / R
    TauAq_ras = H_ras * n / R
    n1_pt = H_pt / (H_pt - Z1_pt)
    n1_ras = H_ras / (H_ras - Z1_ras)
    n2_pt = H_pt / (H_pt - Z2_pt)
    n2_ras = H_ras / (H_ras - Z2_ras)
    ln_n1pt = math.log(n1_pt)
    ln_n1ras = math.log(n1_ras)
    ln_n2pt = math.log(n2_pt)
    ln_n2ras = math.log(n2_ras)

    # equation A4 from TracerLPM, with last term change from 1/n1 to 1/n2.    
    age_points = ((1 / ((1/n1_pt) - (1/n2_pt))) * TauAq_pt * (((1/n1_pt)*ln_n1pt)+(1/n1_pt)-((1/n2_pt)*ln_n2pt)-(1/n2_pt)))
    age_raster = ((1 / ((1/n1_ras) - (1/n2_ras))) * TauAq_ras * (((1/n1_ras)*ln_n1ras)+(1/n1_ras)-((1/n2_ras)*ln_n2ras)-(1/n2_ras)))
      
    well.AGE_pts = age_points
    well.AGE_rast = age_raster
    well.Pt_er = (SA - age_points)
    well.Rst_er = (SA - age_raster)
    wells.updateRow(well)      

arcpy.CheckInExtension("spatial")