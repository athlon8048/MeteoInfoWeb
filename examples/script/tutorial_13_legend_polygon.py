#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-7
# Purpose: Set graduated color legend scheme
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.layout import MapLayout
from org.meteoinfo.data.mapdata import MapDataManage
from org.meteoinfo.data.meteodata import MeteoDataInfo, DrawMeteoData
from org.meteoinfo.legend import LegendManage, LegendType, LegendScheme, PolygonBreak
from org.meteoinfo.layout import LegendStyles
from org.meteoinfo.shape import ShapeTypes
from org.meteoinfo.global import Extent
import os.path
from java.awt import Color
from javax.swing import JFrame

#---- Set directories
print 'Set directories...'
baseDir = 'D:/MyProgram/Distribution/java/MeteoInfo/MeteoInfo'
dataDir = os.path.join(baseDir, 'sample/GrADS')
mapDir = os.path.join(baseDir, 'map')
figDir = 'D:/Temp/test'

#---- Create MapLayout object
mapLayout = MapLayout()
mapFrame = mapLayout.getActiveMapFrame()

#---- Load country layer
print 'Load country layer...'
countryLayer = MapDataManage.loadLayer(os.path.join(mapDir, 'country1.shp'))
lb = countryLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setDrawFill(False)
lb.setOutlineColor(Color.gray)
mapFrame.addLayer(countryLayer)

#---- Open GrADS data
print 'Open GrADS data...'
mdi = MeteoDataInfo()
mdi.openGrADSData(os.path.join(dataDir, 'model.ctl'))

#---- Set time index
mdi.setTimeIndex(2)

#---- Get pressure grid data
gdata = mdi.getGridData('PS')
gdata.extendToGlobal()

#---- Create layer
print 'Create layer...'
ls = LegendScheme(ShapeTypes.Polygon)
ls.setLegendType(LegendType.GraduatedColor)
values = [450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950,1000, 1050]
colors = [Color(160,0,200),Color(110,0,220),Color(30,60,255),Color(0,160,255),Color(0,200,200),Color(0,220,0),
	Color(160,230,50),Color(230,220,50),Color(230,175,45),Color(240,130,40),Color(250,60,60),Color(240,0,130)]
lbs = ls.getLegendBreaks()
for i in range(0, len(colors)):
	lb = PolygonBreak()
	lb.setColor(colors[i])
	lb.setStartValue(values[i])
	lb.setEndValue(values[i + 1])
	lb.setCaption(str(values[i]) + ' ' + str(values[i + 1]))
	lb.setDrawOutline(False)
	lbs.add(lb)

layer = DrawMeteoData.createShadedLayer(gdata, ls, 'Pressure_Shaded', 'PS', True)

#---- Add layer
mapFrame.addLayer(layer)
mapFrame.moveLayer(layer, 0)

#---- Add title
title = mapLayout.addText('MeteoInfo script demo', 350, 30, 'Arial', 16)

#---- Zoom layout map
print 'Zoom layout map...'
mapLayout.getActiveLayoutMap().zoomToExtentLonLatEx(Extent(0, 360, -90, 90))

#---- Set mapframe
mapFrame.setGridXDelt(30)
mapFrame.setGridYDelt(30)

#---- Add legend
legend = mapLayout.addLegend(150, 440)
legend.setLegendStyle(LegendStyles.Bar_Horizontal)
legend.setLegendLayer(layer)

frame = JFrame('MeteoInfo Script Sample', size = (750, 540))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'