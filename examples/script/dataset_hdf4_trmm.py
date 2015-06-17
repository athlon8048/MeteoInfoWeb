#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-7-2
# Purpose: Read TRMM precipitation hdf4 data
# Note: Sample
#-----------------------------------------------------
from org.meteoinfo.data.meteodata import MeteoDataInfo
from org.meteoinfo.data.meteodata import Dimension
from org.meteoinfo.data.meteodata import DimensionType
from org.meteoinfo.data.meteodata import DrawMeteoData
from org.meteoinfo.legend import LegendType
from org.meteoinfo.legend import LegendManage
from org.meteoinfo.shape import ShapeTypes
from ucar.nc2 import NetcdfFile
import os.path
import jarray

#Set data directory
dataDir = 'D:/Temp/hdf'

#Create MeteoDataInfo object
mdi = MeteoDataInfo()

#Read hdf data file
fn = os.path.join(dataDir, '3B43.19980101.7.HDF')
if os.path.isfile(fn):
	print fn
	mdi.openNetCDFData(fn)
	dataInfo = mdi.getDataInfo()
	#print mdi.getInfoText()
	xmin = -180.0
	ymin = -50.0
	xnum = 1440
	ynum = 400
	xdelt = 0.25
	ydelt = 0.25
	xlist = []
	ylist = []
	for i in range(0,xnum):
		xlist.append(xmin + xdelt * i)
	for i in range(0,ynum):
		ylist.append(ymin + ydelt * i)

	X = jarray.array(xlist, 'd')
	Y = jarray.array(ylist, 'd')
	xDim = Dimension(DimensionType.X)
	xDim.setValues(X)
	dataInfo.setXDimension(xDim)
	yDim = Dimension(DimensionType.Y)
	yDim.setValues(Y)
	dataInfo.setYDimension(yDim)
	var = dataInfo.getVariable('precipitation')
	print var.getName()
	dimList = [xDim, yDim]
	var.setDimensions(dimList)
	gData = mdi.getGridData(var.getName())	
	aLS = LegendManage.createLegendSchemeFromGridData(gData, LegendType.GraduatedColor, ShapeTypes.Polygon)
	aLayer = DrawMeteoData.createRasterLayer(gData, "Test_HDF", aLS)
	mf = miapp.getMapDocument().getActiveMapFrame()
	mf.addLayer(aLayer)
	mf.moveLayer(aLayer, 0)	

print 'Finished!'