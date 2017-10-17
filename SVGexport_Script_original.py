import json,requests,urllib2,math

#'''
#pNLFID = arcpy.GetParameterAsText(0)
#pCTL_BEGIN = arcpy.GetParameterAsText(1)
#pCTL_END = arcpy.GetParameterAsText(2)
#'''

pNLFID = 'SFRAIR00270**N'
pCTL_BEGIN = 0
pCTL_END = 3
#imagedimensions = '1200,300'
#imageformat = 'svg'
#outputname = '{}_{}_{}.{}'.format(pNLFID.replace('*','-'),str(pCTL_BEGIN).replace('.','-'),str(pCTL_END).replace('.','-'),imageformat)

dyndata ={'routeId':pNLFID,'fromMeasure':pCTL_BEGIN,'toMeasure':pCTL_END,'f': 'pjson'} # Set the input values for ODOT LRS Tools.

DynSegResp = requests.get("http://collectornew.dot.state.oh.us/arcgis/rest/services/OdotLrsTools/LRS_2015_StateAndRamps/MapServer/exts/OdotDynSegTools/CountyRouteBetweenMs", params=dyndata)

#arcpy.AddMessage(DynSegResp.json())
for feature in DynSegResp.json()['features']:
	geopath = feature['geometry']['paths']
	for point in geopath:
		xlist = []
		ylist = []
		for a in point:
			xlist.append(a[0])
			ylist.append(a[1])

		# Begin and End Coordinates for rotation
		x1 = point[0][0]
		y1 = point[0][1]
		x2 = point[-1][0]
		y2 = point[-1][1]
		rotation = math.degrees(math.atan2(y2 - y1,x2 - x1)) * -1
		print rotation

		# Bounding Box
		boundingbox = '{0},{1},{2},{3}'.format(min(xlist),min(ylist),max(xlist),max(ylist))
		print boundingbox
        boundingbox_big = '{0},{1},{2},{3}'.format(min(xlist)*0.99995,min(ylist)*0.99995,max(xlist)*1.00005,max(ylist)*1.00005)
        print boundingbox_big
#		mapdata = {'bbox':boundingbox,'size':imagedimensions,'format':imageformat,'rotation':rotation,'f':'pjson'}
#		MapExportResp = requests.get("https://collectornew.dot.state.oh.us/arcgis/rest/services/BOUNDARIES/Boundaries/MapServer/export", params=mapdata)
#		file = urllib2.urlopen(MapExportResp.json()['href'])
#		with open(outputname, "wb") as code:
#			code.write(file.read())
#		print 'Saving file {}'.format(outputname)

print'Complete'

