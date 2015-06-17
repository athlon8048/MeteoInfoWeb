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

#---- Load project file (*.mip)
pfn = 'D:/Temp/mip/rain.mip'
mapLayout.loadProjectFile(pfn)
mapFrame = mapLayout.getActiveMapFrame()

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
lsfn = 'D:/Temp/rain1.lgs'
ls.importFromXMLFile(lsfn)

#---- Create shaded layer
print 'Create shaded layer...'	
layer = DrawMeteoData.createShadedLayer(gdata, ls, 'Rain_shaded', 'Rain', True)
layer.setMaskout(True)

#---- Add layer
mapFrame.addLayer(layer)
mapFrame.moveLayer(layer, 0)

#---- Set sub title
stime = stime + timedelta(hours=-6)
subTitle = mapLayout.getTexts().get(1)
subTitle.setLabelText(u'（' + stime.strftime('%Y-%m-%d %H:00') +
	u' 至 ' + etime.strftime('%Y-%m-%d %H:00') + u'）')

#---- Set legend
legend = mapLayout.getLegends().get(0)
legend.setLegendLayer(layer)
legend.setTitle(u'降水量（毫米）')

frame = JFrame('MeteoInfo Script Sample', size = (750, 530))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'