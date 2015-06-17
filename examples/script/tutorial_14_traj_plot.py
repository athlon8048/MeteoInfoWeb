#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-19
# Purpose: Plot HYSPLIT trajectory data
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.layout import MapLayout, PaperSize
from org.meteoinfo.data.mapdata import MapDataManage
from org.meteoinfo.data.meteodata import MeteoDataInfo
from org.meteoinfo.global import Extent
from org.meteoinfo.drawing import PointStyle
from org.meteoinfo.chart import Chart
from org.meteoinfo.chart.plot import XY1DPlot, ChartPlotMethod
import os
from java.awt import Color
from javax.swing import JFrame

#---- Set directories
print 'Set directories...'
baseDir = 'D:/MyProgram/Distribution/java/MeteoInfo/MeteoInfo'
dataDir = os.path.join(baseDir, 'sample')
mapDir = os.path.join(baseDir, 'map')
figDir = 'D:/Temp/test'

#---- Create MapLayout object
mapLayout = MapLayout()
mapFrame = mapLayout.getActiveMapFrame()
ps = PaperSize('Custum', 650, 640)
mapLayout.setPaperSize(ps)

#---- Load country layer
print 'Load country layer...'
countryLayer = MapDataManage.loadLayer(os.path.join(mapDir, 'country1.shp'))
lb = countryLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setOutlineColor(Color.black)
lb.setOutlineSize(2)
mapFrame.addLayer(countryLayer)

#---- Create MeteoDataInfo object
mdi = MeteoDataInfo()

#---- Open a trajectory data file
print 'Open trajectory data file...'
fn = os.path.join(dataDir, 'HYSPLIT/tdump')
mdi.openHYSPLITTrajData(fn)
dataInfo = mdi.getDataInfo()

#---- Create trajectory layers
print 'Create trajectory layers...'
trajLayer = dataInfo.createTrajLineLayer()
startLayer = dataInfo.createTrajStartPointLayer()
lb = startLayer.getLegendScheme().getLegendBreaks().get(0)
lb.setStyle(PointStyle.Star)

#---- Add layer
mapFrame.addLayer(trajLayer)
mapFrame.addLayer(startLayer)

#---- Add pressure profile chart
print 'Add pressure profile chart...'
dataset = dataInfo.getXYDataset(12)    #Pressure is in 12th column
plot = XY1DPlot(True, dataset)
plot.setChartPlotMethod(ChartPlotMethod.LINE_POINT)
plot.getXAxis().setLabel('Time')
plot.getYAxis().setLabel('hPa')
plot.getYAxis().setInverse(True)
ls = trajLayer.getLegendScheme()
for i in range(0, dataset.getSeriesCount()):
	plot.setLegendBreak(i, ls.getLegendBreaks().get(i))
chart = Chart(None, plot)
chart.setDrawLegend(False)
layoutChart = mapLayout.addChart(5, 410)
layoutChart.setWidth(600)
layoutChart.setHeight(200)
layoutChart.setChart(chart)

#---- Add title
title = mapLayout.addText('MeteoInfo script demo - Trajectory', 300, 30, 'Arial', 16)

#---- Zoom map
print 'Zoom map...'
mapLayout.getActiveLayoutMap().setWidth(550)
mapLayout.getActiveLayoutMap().setHeight(350)
mapFrame.getMapView().zoomToExtent(trajLayer.getExtent().extend(2, 2))

#---- Output figure
print 'Output figure...'
mapLayout.exportToPicture(os.path.join(figDir, 'traj_test.png'))

#---- Set mapframe
mapFrame.setGridXDelt(5)
mapFrame.setGridYDelt(5)

#---- Show result from (just for check and not needed for batch run)
frame = JFrame('MeteoInfo Script Sample', size = (650, 680))
frame.add(mapLayout)
frame.visible = True

print 'Finish...'