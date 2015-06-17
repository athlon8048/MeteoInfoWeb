#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-6
# Purpose: Get and plot station wind data
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.layout import MapLayout
from org.meteoinfo.data.mapdata import MapDataManage
from org.meteoinfo.data.meteodata import MeteoDataInfo, DrawMeteoData
from org.meteoinfo.layout import LegendStyles
from org.meteoinfo.global import Extent
import os
from java.awt import Color
from javax.swing import JFrame

#---- Set directories
print 'Set directories...'
baseDir = 'D:/MyProgram/Distribution/java/MeteoInfo/MeteoInfo'
dataDir = os.path.join(baseDir, 'sample')
mapDir = os.path.join(baseDir, 'map')

#---- Create MapLayout object
mapLayout = MapLayout()
mapFrame = mapLayout.getActiveMapFrame()

#---- Load country layer
print 'Load country layer...'
countryLayer = MapDataManage.loadLayer(os.path.join(mapDir, 'country1.shp'))
lb = countryLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setDrawFill(False)
lb.setOutlineColor(Color.black)
mapFrame.addLayer(countryLayer)

#---- Create MeteoDataInfo object
mdi = MeteoDataInfo()

#---- Open a MICAPS data file
fn = os.path.join(dataDir, 'MICAPS/10101414.000')
mdi.openMICAPSData(fn)

#---- Get wind direction/speed station data
windDir = mdi.getStationData('WindDirection')
windSpeed = mdi.getStationData('WindSpeed')

#---- Create barb and vector wind layers
bLayer = DrawMeteoData.createSTBarbLayer(windDir, windSpeed, 'WindBarb_Point', False)
vLayer = DrawMeteoData.createSTVectorLayer(windDir, windSpeed, 'WindVector_Point', False)

#---- Add layers
mapFrame.addLayer(bLayer)
mapFrame.addLayer(vLayer)

#---- Add title
title = mapLayout.addText('MeteoInfo script demo', 350, 30, 'Arial', 16)

#---- Set layout map
print 'Set layout map...'
mapLayout.getActiveLayoutMap().setWidth(580)
mapLayout.getActiveLayoutMap().zoomToExtentLonLatEx(Extent(70, 140, 15, 55))

#---- Set mapframe
mapFrame.setGridXDelt(10)
mapFrame.setGridYDelt(10)

frame = JFrame('MeteoInfo Script Sample', size = (800, 600))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'