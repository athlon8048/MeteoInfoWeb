#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2013-12-5
# Purpose: Read MODIS AOD hdf4 data
# Note: Sample
#-----------------------------------------------------
from org.meteoinfo.data.meteodata import MeteoDataInfo
from org.meteoinfo.data.meteodata import Dimension
from org.meteoinfo.data.meteodata import DimensionType
from org.meteoinfo.data.meteodata import DrawMeteoData
from org.meteoinfo.legend import LegendScheme
from org.meteoinfo.shape import ShapeTypes
from ucar.nc2 import NetcdfFile
import os.path
import jarray

#Set data directory
dataDir = 'D:/Temp/toMingJing/AOD'
outDir = 'D:/Temp'

#Create MeteoDataInfo object
mdi = MeteoDataInfo()

#Read hdf data file
fn = os.path.join(dataDir, 'MOD08_M3.A2000061.051.2010273213159.pscs_000500501908.Optical_Depth_Land_And_Ocean_Mean_Mean.G3.HDF')
if os.path.isfile(fn):
	print fn
	mdi.openNetCDFData(fn)
	dataInfo = mdi.getDataInfo()
	#print mdi.getInfoText()
	xmin = -180.0
	ymin = -90.0
	xnum = 360
	ynum = 180
	xdelt = 1.0
	ydelt = 1.0
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
	var = dataInfo.getVariable('Optical_Depth_Land_And_Ocean_Mean_Mean')
	print var.getName()
	dimList = [yDim, xDim]
	var.setDimensions(dimList)
	gData = mdi.getGridData(var.getName())	
	#aLS = LegendManage.createLegendSchemeFromGridData(gData, LegendType.GraduatedColor, ShapeTypes.Polygon)
	aLS = LegendScheme(ShapeTypes.Polygon)
	aLS.importFromXMLFile(os.path.join(dataDir, 'AOD.lgs'))
	aLayer = DrawMeteoData.createRasterLayer(gData, "Test_HDF", aLS)
	mf = miapp.getMapDocument().getActiveMapFrame()
	mf.addLayer(aLayer)
	mf.moveLayer(aLayer, 0)
	mdi = MeteoDataInfo()
	inf = os.path.join(outDir, 'China_Prec_2010101420.csv')
	outf = os.path.join(outDir, 'test.csv')
	mdi.openLonLatData(inf)
	stData = mdi.getStationData('Precipitation')
	interData = gData.toStation(stData)
	interData.saveAsCSVFile(outf, 'AOD')

print 'Finished!'