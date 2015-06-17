# coding=utf-8
#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-11-30
# Purpose: Open a NetCDF data file and show data information
# Note: Sample
#-----------------------------------------------------
#---- Import classes
print 'Import classes...'
from org.meteoinfo.data.meteodata import MeteoDataInfo
import os

#---- Set directories
print 'Set directories...'
baseDir = 'D:/MyProgram/Distribution/java/MeteoInfo/MeteoInfo'
dataDir = os.path.join(baseDir, 'sample')

#---- Create MeteoDataInfo object
mdi = MeteoDataInfo()

#---- Open a NetCDF data file
fn = os.path.join(dataDir, 'NetCDF/air.mon.ltm.nc')
mdi.openNetCDFData(fn)

#---- Show data information
print mdi.getInfoText()

print 'Finished!'