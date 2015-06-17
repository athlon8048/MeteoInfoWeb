#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2013-10-29
# Purpose: Read hdf4 data
# Note: Sample
#-----------------------------------------------------
from org.meteoinfo.data.meteodata import MeteoDataInfo
from org.meteoinfo.data.meteodata import Dimension
from org.meteoinfo.data.meteodata import DimensionType
from org.meteoinfo.data.meteodata import DrawMeteoData
from org.meteoinfo.projection import ProjectionInfo
from org.meteoinfo.legend import LegendManage
from org.meteoinfo.legend import LegendType
from org.meteoinfo.shape import ShapeTypes
import os.path
import jarray

#Set data directory
dataDir = 'D:/Temp/hdf/'

#Create MeteoDataInfo object
mdi = MeteoDataInfo()

#Read hdf data file
fn = dataDir + 'S19972441997273.L3m_MO_CHL_chlor_a_9km'
if os.path.isfile(fn):
	print fn
	mdi.openNetCDFData(fn)
	dataInfo = mdi.getDataInfo()
	print mdi.getInfoText()
	xmin = -180.0
	ymin = -90.0
	xnum = 4320
	ynum = 2160
	xdelt = 0.083333336
	ydelt = 0.083333336
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
	var = dataInfo.getVariable('l3m_data')
	dimList = [yDim, xDim]
	var.setDimensions(dimList)
	gData = mdi.getGridData(var.getName())
	gData.yReverse()
	gData.missingValue = -32767.0
	aLS = LegendManage.createLegendSchemeFromGridData(gData, LegendType.GraduatedColor, ShapeTypes.Polygon)
	aLayer = DrawMeteoData.createRasterLayer(gData, "Test_HDF", aLS)
	aLayer.setProjInfo(dataInfo.getProjectionInfo())
	mf = miapp.getMapDocument().getActiveMapFrame()
	mf.addLayer(aLayer)
	mf.moveLayer(aLayer, 0)

print 'Finished!'