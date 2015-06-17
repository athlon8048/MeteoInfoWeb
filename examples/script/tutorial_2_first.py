#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-11-22
# Purpose: Read GrADS data and plot
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.layout import MapLayout
from org.meteoinfo.data.mapdata import MapDataManage
from org.meteoinfo.data.meteodata import MeteoDataInfo, DrawMeteoData
from org.meteoinfo.legend import LegendManage, LegendType, GridLabelPosition
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
lb.setOutlineColor(Color.blue)
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

#---- Create pressure shaded layer
print 'Create pressure shaded layer...'
pressLayer = DrawMeteoData.createShadedLayer(gdata, 'Pressure', 'PS', True)

#---- Add layer
mapFrame.addLayer(pressLayer)

#--- Move pressure layer to bottom
mapFrame.moveLayer(pressLayer, 0)

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
legend.setLegendLayer(pressLayer)

#---- Output figure
print 'Output figure...'
mapLayout.paintGraphics()
mapLayout.exportToPicture(os.path.join(figDir, 'pressure_test.ps'))

frame = JFrame('MeteoInfo Script Sample', size = (750, 540))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'