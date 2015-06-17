# encoding=utf-8
#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-6
# Purpose: Interpolate station data to grid data
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.layout import MapLayout
from org.meteoinfo.data import StationData
from org.meteoinfo.data.mapdata import MapDataManage
from org.meteoinfo.data.meteodata import MeteoDataInfo, DrawMeteoData
from org.meteoinfo.legend import LegendScheme, LegendType, PolygonBreak, MapFrame
from org.meteoinfo.shape import ShapeTypes
from org.meteoinfo.layout import LegendStyles, LayoutMap
from org.meteoinfo.global import Extent
from org.meteoinfo.projection import ProjectionInfo
from org.meteoinfo.geoprocess.analysis import InterpolationSetting
import os
from datetime import datetime
from datetime import timedelta
from java.awt import Color
from java.awt import Font
from javax.swing import JFrame

#---- Set directories
print 'Set directories...'
baseDir = 'D:/MyProgram/Distribution/java/MeteoInfo/MeteoInfo'
dataDir = os.path.join(baseDir, 'sample/MICAPS')
mapDir = os.path.join(baseDir, 'map')

#---- Create MapLayout object
mapLayout = MapLayout()
mapFrame = mapLayout.getActiveMapFrame()
mapView = mapFrame.getMapView()
layoutMap = mapLayout.getActiveLayoutMap()

#---- Load layers
print 'Load layers...'
bou2Layer = MapDataManage.loadLayer(os.path.join(mapDir, 'bou2_4p.shp'))
lb = bou2Layer.getLegendScheme().getLegendBreaks().get(0)
lb.setDrawFill(False)
lb.setOutlineColor(Color.gray)
mapFrame.addLayer(bou2Layer)
bou1Layer = MapDataManage.loadLayer(os.path.join(mapDir, 'bou1_4l.shp'))
lb = bou1Layer.getLegendScheme().getLegendBreaks().get(0)
lb.setColor(Color.blue)
mapFrame.addLayer(bou1Layer)
bou1Layer_1 = MapDataManage.loadLayer(os.path.join(mapDir, 'bou1_4l.shp'))
lb = bou1Layer_1.getLegendScheme().getLegendBreaks().get(0)
lb.setColor(Color.blue)
chinaLayer = MapDataManage.loadLayer(os.path.join(mapDir, 'china.shp'))
chinaLayer.setVisible(False)
mapFrame.addLayer(chinaLayer)
cityLayer = MapDataManage.loadLayer(os.path.join(mapDir, 'res1_4m.shp'))
lb = cityLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setSize(6)
lb.setColor(Color.red)
labset = cityLayer.getLabelSet()
labset.setFieldName('NAME')
font = Font(u'楷体', Font.PLAIN, 16)
labset.setLabelFont(font)
labset.setYOffset(15)
cityLayer.addLabels()
mapFrame.addLayer(cityLayer)

#---- Add South China Sea
aMapFrame = MapFrame()
aLayoutMap = LayoutMap(aMapFrame)
aLayoutMap.setDrawGridLabel(False)
aLayoutMap.setDrawGridTickLine(False)
aLayoutMap.setLeft(40)
aLayoutMap.setTop(350)
aLayoutMap.setWidth(85)
aLayoutMap.setHeight(109)
mapLayout.addElement(aLayoutMap)
aMapFrame.addLayer(bou1Layer_1)
aProjInfo = ProjectionInfo("+proj=lcc+lat_1=25+lat_2=47+lon_0=105")
aMapFrame.getMapView().projectLayers(aProjInfo)
aMapFrame.getMapView().zoomToExtentLonLatEx(Extent(106.5,122.5,1,23))

#---- Project mapview
print 'Project mapview...'
projStr = '+proj=lcc+lat_1=25+lat_2=47+lon_0=105'
projInfo = ProjectionInfo(projStr)
mapView.projectLayers(projInfo)
extent = Extent(78,130,15,53)
mapView.zoomToExtentLonLatEx(extent)

#---- Create MeteoDataInfo object
mdi = MeteoDataInfo()

#---- Set start/end time
stime = datetime(2010,10,14,14)
etime = datetime(2010,10,14,20)

#---- Loop
print 'Get sum station data...'
sdata = StationData()
atime = stime
i = 0
while atime < etime:
	#---- Open a MICAPS data file
	fn = os.path.join(dataDir, stime.strftime('%y%m%d%H') + '.000')
	mdi.openMICAPSData(fn)

	#---- Sum precipitation station data
	if i == 0:
		sdata = mdi.getStationData('Precipitation6h')
	else:
		sdata = sdata.add(mdi.getStationData('Precipitation6h'))

	atime = atime + timedelta(hours=6)
	
#---- Interpolate station data to grid data
print 'Interpolate station data to grid data...'
interpSet = InterpolationSetting(60,140,-20,60,160,160,"IDW_Radius",2,1)
#radList = [10.0, 8.0, 6.0, 4.0]
#interpSet = InterpolationSetting(60,140,-20,60,160,160,"Cressman",radList)
gdata = sdata.interpolateData(interpSet)

#---- Set legend scheme
ls = LegendScheme(ShapeTypes.Polygon)
ls.setLegendType(LegendType.GraduatedColor)
values = [0,0.1,1,2,5,10,20,25,50,100,1000]
colors = [Color(255,255,255),Color(170,240,255),Color(120,230,240),Color(200,220,50),Color(240,220,20),
	Color(255,120,10),Color(255,90,10),Color(240,40,0),Color(180,10,0),Color(120,10,0)]
lbs = ls.getLegendBreaks()
for i in range(0, len(colors)):
	lb = PolygonBreak()
	lb.setColor(colors[i])
	lb.setStartValue(values[i])
	lb.setEndValue(values[i + 1])
	if i == 0:
		lb.setCaption('< ' + str(values[i + 1]))
	elif i == len(colors) - 1:
		lb.setCaption('> ' + str(values[i]))
	else:
		lb.setCaption(str(values[i]) + ' - ' + str(values[i + 1]))
	lb.setDrawOutline(False)
	lbs.add(lb)

#---- Create shaded layer
print 'Create shaded layer...'	
layer = DrawMeteoData.createShadedLayer(gdata, ls, 'Rain_shaded', 'Rain', True)
layer.setMaskout(True)

#---- Add layer
mapFrame.addLayer(layer)
mapFrame.moveLayer(layer, 0)

#---- Add title
title = mapLayout.addText('Precipitation map of China', 280, 40, 'Arial', 18)
stime = stime + timedelta(hours=-6)
subTitle = mapLayout.addText('(' + stime.strftime('%Y-%m-%d %H:00') +
	' to ' + etime.strftime('%Y-%m-%d %H:00') + ')', 280, 60, 'Arial', 16)

#---- Set layout map
print 'Set layout map...'
layoutMap.setDrawGridLine(False)
layoutMap.setDrawNeatLine(False)
layoutMap.setDrawGridLabel(False)
layoutMap.setDrawGridTickLine(False)
layoutMap.setLeft(10)
layoutMap.setTop(10)
layoutMap.setWidth(620)
layoutMap.setHeight(450)

#---- Set maskout
mapView.getMaskOut().setMask(True)
mapView.getMaskOut().setMaskLayer(chinaLayer.getLayerName())

#---- Set mapframe
mapFrame.setGridXDelt(10)
mapFrame.setGridYDelt(10)

#---- Add legend
legend = mapLayout.addLegend(575, 250)
legend.setLegendStyle(LegendStyles.Normal)
legend.setLegendLayer(layer)
legend.setFont(Font('Arial', Font.PLAIN, 12))
legend.setTitle('Precipitation (mm)')

frame = JFrame('MeteoInfo Script Sample', size = (750, 530))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'