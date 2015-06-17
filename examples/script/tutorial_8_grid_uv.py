#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-1
# Purpose: Read and plot U/V grid data
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

#---- Open a GrADS data file
fn = os.path.join(dataDir, 'GrADS/model.ctl')
mdi.openGrADSData(fn)

#---- Get U/V grid data
mdi.setTimeIndex(2)
mdi.setLevelIndex(3)
udata = mdi.getGridData('U')
vdata = mdi.getGridData('V')

#---- Create wind vector layer from the U/V grid data
layer = DrawMeteoData.createGridVectorLayer(udata, vdata,  'UV_Vector', True)
#layer = DrawMeteoData.createGridBarbLayer(udata, vdata,  'UV_Barb', True)
#layer = DrawMeteoData.createStreamlineLayer(udata, vdata, 'Z_Streamline', True)

#---- Add layer
mapFrame.addLayer(layer)

#--- Move pressure layer to bottom
mapFrame.moveLayer(layer, 0)

#---- Add title
title = mapLayout.addText('MeteoInfo script demo', 350, 30, 'Arial', 16)

#---- Add wind arrow
windArrow = mapLayout.addWindArrow(660, 420)

#---- Zoom layout map
print 'Zoom layout map...'
mapLayout.getActiveLayoutMap().zoomToExtentLonLatEx(Extent(70, 140, 15, 55))

#---- Set mapframe
mapFrame.setGridXDelt(10)
mapFrame.setGridYDelt(10)

frame = JFrame('MeteoInfo Script Sample', size = (800, 600))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'