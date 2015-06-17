#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-11-30
# Purpose: Get and plot grid data
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
lb.setOutlineColor(Color.blue)
mapFrame.addLayer(countryLayer)

#---- Create MeteoDataInfo object
mdi = MeteoDataInfo()

#---- Open a GrADS data file
fn = os.path.join(dataDir, 'GrADS/model.ctl')
mdi.openGrADSData(fn)

#---- Get grid data
mdi.setTimeIndex(2)
mdi.setLevelIndex(3)
gdata = mdi.getGridData('Z')
gdata.extendToGlobal()

#---- Create shaded layer from the grid data
layer = DrawMeteoData.createContourLayer(gdata, 'Z_contour', 'Z', True)
#layer = DrawMeteoData.createShadedLayer(gdata, 'Z_shaded', 'Z', True)
#layer = DrawMeteoData.createRasterLayer(gdata, 'Z_raster')
#layer = DrawMeteoData.createGridFillLayer(gdata, 'Z_gridfill', 'Z')
#layer = DrawMeteoData.createGridPointLayer(gdata, 'Z_gridpoint', 'Z')

#---- Add layer
mapFrame.addLayer(layer)

#--- Move pressure layer to bottom
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

frame = JFrame('MeteoInfo Script Sample', size = (800, 600))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'