#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-11-25
# Purpose: Load layer
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.layout import MapLayout
from org.meteoinfo.data.mapdata import MapDataManage
from org.meteoinfo.global import Extent
import os.path
from java.awt import Color
from javax.swing import JFrame

#---- Set directories
print 'Set directories...'
baseDir = 'D:/MyProgram/Distribution/java/MeteoInfo/MeteoInfo'
mapDir = os.path.join(baseDir, 'map')

#---- Create MapLayout object
mapLayout = MapLayout()
mapFrame = mapLayout.getActiveMapFrame()

#---- Load layers
print 'Load image layer...'
fn = os.path.join(mapDir, 'GLOBALeb3colshade.jpg')
imageLayer = MapDataManage.loadLayer(fn)
mapFrame.addLayer(imageLayer)

print 'Load country layer...'
fn = os.path.join(mapDir, 'country1.shp')
countryLayer = MapDataManage.loadLayer(fn)
lb = countryLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setDrawFill(False)
lb.setOutlineColor(Color.black)
mapFrame.addLayer(countryLayer)

print 'Load river layer...'
fn = os.path.join(mapDir, 'rivers.shp')
riverLayer = MapDataManage.loadLayer(fn)
lb = riverLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setColor(Color.blue)
lb.setSize(1.5)
mapFrame.addLayer(riverLayer)

print 'Load city layer...'
cityLayer = MapDataManage.loadLayer(os.path.join(mapDir, 'res1_4m.shp'))
lb = cityLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setSize(6)
lb.setColor(Color.red)
mapFrame.addLayer(cityLayer)

#---- Add title
title = mapLayout.addText('MeteoInfo script demo', 350, 30, 'Arial', 16)

#---- Zoom layout map
print 'Zoom layout map...'
mapLayout.getActiveLayoutMap().zoomToExtentLonLatEx(Extent(70, 140, 15, 55))

#---- Set mapframe
mapFrame.setGridXDelt(10)
mapFrame.setGridYDelt(10)
mapLayout.paintGraphics()

frame = JFrame('MeteoInfo Script Sample', size = (800, 600))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'