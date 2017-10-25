import json,requests,urllib2,math

#'''
#pNLFID = arcpy.GetParameterAsText(0)
#pCTL_BEGIN = arcpy.GetParameterAsText(1)
#pCTL_END = arcpy.GetParameterAsText(2)
#'''

pNLFID = 'SFRAIR00270**N'
pCTL_BEGIN = 36
pCTL_END = 39
#while pCTL_BEGIN < 52:
    
imagedimensions = '1200,500'
imageformat = 'svg'
outputname = '{}_{}_{}.{}'.format(pNLFID.replace('*','-'),str(pCTL_BEGIN).replace('.','-'),str(pCTL_END).replace('.','-'),imageformat)

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
    dist = math.hypot(max(xlist)-min(xlist),max(ylist)-min(ylist))
    print rotation
#       print dist
    # Bounding Box
#    boundingbox = '{0},{1},{2},{3}'.format(min(xlist),min(ylist),max(xlist),max(ylist))
#    print boundingbox
    xmin = (min(xlist) + max(xlist))/2-(dist/2)
    xmax = (min(xlist) + max(xlist))/2+(dist/2)
    ymin = (min(ylist) + max(ylist))/2+(dist/4.8)-(dist/4.8)
    ymax = (min(ylist) + max(ylist))/2+(dist/4.8)q+(dist/4.8)
    boundingbox = '{0},{1},{2},{3}'.format(xmin,ymin,xmax,ymax)
#    boundingbox = '{0},{1},{2},{3}'.format(xmin-240,ymin-100,xmax+240,ymax+100)
    print boundingbox
#            mapdata = {'bbox':boundingbox,'size':imagedimensions,'format':imageformat,'rotation':rotation,'f':'pjson'}
#            MapExportResp = requests.get("https://collectornew.dot.state.oh.us/arcgis/rest/services/BOUNDARIES/Boundaries/MapServer/export", params=mapdata)
#            file = urllib2.urlopen(MapExportResp.json()['href'])
#            with open("export/"+outputname, "wb") as code:
#                code.write(file.read())
#                print 'Saving file {}'.format(outputname)
#    pCTL_BEGIN+=3
#    pCTL_END+=3
print'Complete'

