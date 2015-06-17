#--------------------------------------------------------        
# Author: Yaqiang Wang                                           
# Date: 2014-10-24                                               
# Purpose: Convert GRIB data to ARL data  
# Note: Sample                                                   
#-----------------------------------------------------------
from org.meteoinfo.data.meteodata import MeteoDataInfo
from org.meteoinfo.data.meteodata.arl import ARLDataInfo
from org.meteoinfo.data.meteodata.arl import DataLabel
import os

#---- Set directories
dataDir = "D:/Temp"

#---- Set output data file
outFile = os.path.join(dataDir, 'arl/test2.arl')

#---- Read a GRIB data file
mydata = MeteoDataInfo()
infile = os.path.join(dataDir, 'grib/201001011800.pgbh06.gdas.20100101-20100105.grb2')
print infile
mydata.openNetCDFData(infile)
print 'GRIB file has been opened...'

#---- Set output ARL data info
arlDI = ARLDataInfo()

#---- Set variable and level list
gvars = ['Pressure_surface','Temperature_height_above_ground',\
	'u-component_of_wind_height_above_ground','v-component_of_wind_height_above_ground',\
	'Geopotential_height_isobaric','Temperature_isobaric',\
	'u-component_of_wind_isobaric','v-component_of_wind_isobaric','Vertical_velocity_pressure_isobaric',\
	'Relative_humidity_isobaric']
avars = ['PRSS','T02M','U10M','V10M','HGTS','TEMP','UWND','VWND','WWND','RELH']
levels = [0,1000,975,950,925,900,875,850,825,800,775,750,700,\
	650,600,550,500,450,400,350,300,250,225,200,175,150,\
	125,100,70,50,30,20,10,7,5,3,2,1]
for l in levels:
	arlDI.levels.add(l)
	if l == 0:
		arlDI.LevelVarList.add(['PRSS','T02M','U10M','V10M'])
	else:
		arlDI.LevelVarList.add(['HGTS','TEMP','UWND','VWND','WWND','RELH'])

#---- Write ARL data file
dataInfo = mydata.getDataInfo()
arlDI.createDataFile(outFile)
arlDI.X = dataInfo.getXDimension().getValues()
arlDI.Y = dataInfo.getYDimension().getValues()
variables = dataInfo.getVariables()
tNum = dataInfo.getTimeNum()
for t in range(0, tNum):
	mydata.setTimeIndex(t)
	atime = dataInfo.getTimes().get(t)
	aDH = arlDI.getDataHead(mydata.getProjectionInfo(), 'FNL1', 2)
	arlDI.writeIndexRecord(atime, aDH)
	lidx = 0
	for l in arlDI.levels:
		print l
		for v in arlDI.LevelVarList[lidx]:
			vName = gvars[avars.index(v)]
			print vName
			if lidx == 0:
				mydata.setLevelIndex(lidx)
			else:
				variable = dataInfo.getVariable(vName)
				nlidx = variable.getZDimension().getDimValue().indexOf(l*100.0)
				mydata.setLevelIndex(nlidx)
			gData = mydata.getGridData(vName)
			if v == 'PRSS' or v == 'WWND':
				gData = gData.divide(100)			
			aDL = DataLabel(atime)
			aDL.setLevel(lidx)
			aDL.setVarName(v)
			aDL.setGrid(99)
			aDL.setForecast(0)
			arlDI.writeGridData(aDL, gData)
		lidx += 1

arlDI.closeDataFile()

print 'Finished!'