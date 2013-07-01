Installation and operation of the Groundwater Age Stratigraphy tool for ARCgis
Paul Juckem, June 10, 2013


Installation:
1) Extract all files in the *.zip file into a local directory with read/write access.
2) If using ArcMap10.1 (possibly 10.0):
	a)Open the example.mxd file and proceed to the "Operation" Section below.  
3) If using an earlier version than ArcMap10.1:
	a) Open an new empty ARCmap file.  Optionally, you can add the example raster files to your new empty ArcMap file.
	b) From ArcMap, open the tool box.  Right-click anywhere within the tool box and select "add new toolbox".
	c) Browse to the extracted directory and add the GWAS93 toolbox ("GWAS93.tbx" file).
	d) Click on the "+" symbol next to the tool box.  Double click the script tool "Groundwater Age Stratigraphy" and follow the "operation" section below.
	
	
Operation:
1) Double-click on the "Groundwater Age Stratigraphy" script tool.
2) Specify the raster input for the water table (eg: "uwspheads") and aquifer base (eg: "uwspl1bot"). Enter a porosity value and either a value for recharge or a raster for recharge (eg: "uwsprecharge").  Specify a percent depth and an output raster. Click "OK."
3) Add the result raster if it's not added automatically.  The raster values will be the computed groundwater age.