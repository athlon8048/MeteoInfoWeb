#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-20
# Purpose: Calculate water vapor flux
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.layout import MapLayout
from org.meteoinfo.data import DataMath
from org.meteoinfo.data.mapdata import MapDataManage
from org.meteoinfo.data.meteodata import MeteoDataInfo, DrawMeteoData
from org.meteoinfo.legend import LegendManage, LegendType
from org.meteoinfo.layout import LegendStyles
from org.meteoinfo.global import Extent
import os.path
from java.text import SimpleDateFormat
from java.awt import Color
from javax.swing import JFrame

#---- Set directories
print 'Set directories...'
baseDir = 'D:/MyProgram/Distribution/java/MeteoInfo/MeteoInfo'
dataDir = 'D:/Temp/nc'
mapDir = os.path.join(baseDir, 'map')

#---- Create MapLayout object
mapLayout = MapLayout()
mapFrame = mapLayout.getActiveMapFrame()
layoutMap = mapLayout.getActiveLayoutMap()

#---- Load country layer
print 'Load country layer...'
countryLayer = MapDataManage.loadLayer(os.path.join(mapDir, 'country1.shp'))
lb = countryLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setDrawFill(False)
lb.setOutlineColor(Color.blue)
mapFrame.addLayer(countryLayer)

#---- Open netCDF data files
print 'Open netCDF data files...'
dataAir = MeteoDataInfo()
dataUwnd = MeteoDataInfo()
dataVwnd = MeteoDataInfo()
dataRhum = MeteoDataInfo()
dataAir.openNetCDFData(os.path.join(dataDir, 'air.2011.nc'))
dataUwnd.openNetCDFData(os.path.join(dataDir, 'uwnd.2011.nc'))
dataVwnd.openNetCDFData(os.path.join(dataDir, 'vwnd.2011.nc'))
dataRhum.openNetCDFData(os.path.join(dataDir, 'rhum.2011.nc'))

#---- Calculation
#---- Set date to June 23
#tIdx = 171
tIdx = 173
dataAir.setTimeIndex(tIdx);
dataUwnd.setTimeIndex(tIdx);
dataVwnd.setTimeIndex(tIdx);
dataRhum.setTimeIndex(tIdx);

#---- Set level to 700hPa
lIdx = 3
dataAir.setLevelIndex(lIdx);
dataUwnd.setLevelIndex(lIdx);
dataVwnd.setLevelIndex(lIdx);
dataRhum.setLevelIndex(lIdx);

#---- Get grid data
print 'Get grid data...'
air = dataAir.getGridData('air')
uwnd = dataUwnd.getGridData('uwnd')
vwnd = dataVwnd.getGridData('vwnd')
rhum = dataRhum.getGridData('rhum')

#---- Calculate
print 'Calculation...'
prs = 700
g = 9.8
es = DataMath.exp(air.sub(273.16).mul(17.67).div(air.sub(29.65))).mul(6.112)
#es = 6.112*DataMath.exp(17.67*(air-273.16)/(air-29.65))
qs = es.mul(0.62197).div(DataMath.sub(prs, es.mul(0.378)))
#qs = 0.62197*es/(prs-0.378*es)
q = qs.mul(rhum).div(100)
#q = qs*rhum/100
qhdivg = DataMath.hdivg(q.mul(uwnd).div(g), q.mul(vwnd).div(g))
#qhdivg = DataMath.Hdivg(q*uwnd/g,q*vwnd/g)
qv = rhum.mul(es).div(100)
#qv = rhum*es/100
uv = DataMath.magnitude(uwnd, vwnd)
#uv = DataMath.Magnitude(uwnd, vwnd)
uvq = uv.mul(qv).div(9.8*1000)
#uvq = uv*qv/(9.8*1000)

#---- Create data layer
print 'Create data layer...'
dataLayer = DrawMeteoData.createShadedLayer(qhdivg, "WaterVaporFlux", "Flux", False)

#---- Add layer
print 'Add layers...'
mapFrame.addLayer(dataLayer)
mapFrame.moveLayer(dataLayer, 0)
#---- Zoom data
mapLayout.getActiveLayoutMap().zoomToExtentLonLatEx(Extent(0,360,-90.1,90.1))
#---- Set MapLayout
format = SimpleDateFormat('yyyy-MM-dd')
aTime = dataAir.getDataInfo().getTimes().get(tIdx)
mapLayout.addText('Water Vapor Flux Divergence - ' + format.format(aTime), 320, 30, 'Arial', 16)
aLegend = mapLayout.addLegend(650, 100)
aLegend.setLegendStyle(LegendStyles.Bar_Vertical)
aLegend.setLegendLayer(dataLayer)
layoutMap.setGridXDelt(60)
layoutMap.setGridYDelt(30)
layoutMap.setDrawGridLine(False)
mapLayout.paintGraphics()

frame = JFrame('MeteoInfo Script Sample', size = (750, 530))
frame.add(mapLayout)
frame.visible = True
print 'Finished!'