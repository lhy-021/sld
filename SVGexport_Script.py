import arcpy,requests,urllib2,math

'''
pNLFID = arcpy.GetParameterAsText(0)
pCTL_BEGIN = arcpy.GetParameterAsText(1)
pCTL_END = arcpy.GetParameterAsText(2)
'''

pNLFID = 'SFRAIR00070**N'
pCTL_BEGIN = 12
pCTL_END = 14
imagedimensions = '1200,500'
imageformat = 'svg'

outputname = '{}_{}_{}.{}'.format(pNLFID.replace('*','-'),str(pCTL_BEGIN).replace('.','-'),str(pCTL_END).replace('.','-'),imageformat)

dyndata ={'routeId':pNLFID,'fromMeasure':pCTL_BEGIN,'toMeasure':pCTL_END,'f': 'pjson'} # Set the input values for ODOT LRS Tools.

DynSegResp = requests.get("http://collectornew.dot.state.oh.us/arcgis/rest/services/OdotLrsTools/LRS_2015_StateAndRamps/MapServer/exts/OdotDynSegTools/CountyRouteBetweenMs", params=dyndata)

#arcpy.AddMessage(DynSegResp.json())
spatialref = DynSegResp.json()['spatialReference']
geometryType = DynSegResp.json()['geometryType']
print spatialref
print geometryType
for feature in DynSegResp.json()['features']:
    #print feature
    esri_json = {}
    print 'MMin: {}'.format(feature['attributes']['MMin'])
    print 'MMax: {}'.format(feature['attributes']['MMax'])
    geopath = feature['geometry']['paths']
    esri_json['paths'] = geopath
    esri_json['spatialReference'] = spatialref

    polyline = arcpy.AsShape(esri_json, True)
    print polyline.extent
    XtrueCentroid = str(polyline.trueCentroid).split()[0]
    YtrueCentroid = str(polyline.trueCentroid).split()[1]

    xlist = []
    ylist = []
    for point in geopath:
        for a in point:
            xlist.append(a[0])
            ylist.append(a[1])
        # Begin and End Coordinates for rotation

    x1 = xlist[0]
    y1 = ylist[0]
    x2 = xlist[-1]
    y2 = ylist[-1]

    rotation = math.degrees(math.atan2(y2 - y1,x2 - x1)) * -1
    dist = math.hypot(x2 - x1, y2 - y1)
    mapScale = dist * 3.2
    print 'Distance between Points: {}'.format(dist)
    print 'Rotation of Points: {}'.format(rotation)

    # Bounding Box
    boundingbox = '{0},{1},{2},{3}'.format(XtrueCentroid,YtrueCentroid,XtrueCentroid,YtrueCentroid)
    #boundingbox = '{0},{1},{2},{3}'.format(min(xlist),min(ylist),max(xlist),max(ylist))
    print "BoundingBox: {}".format(boundingbox)
    #centerx = (max(xlist) + min(xlist))/2
    #centery = (max(ylist) + min(ylist))/2
    #boundingbox1 = '{},{},{},{}'.format(centerx,centery,centerx,centery)
    #boundingbox2 = '-9259508.766313432,4858689.534183882,-9259508.766313432,4858689.534183882'
    #print "BoundingBox Calculated Center Points: {}".format(boundingbox1)
    #print "BoundingBox Actual Center Points:     {}".format(boundingbox2)

    mapdata = {'bbox':boundingbox,'mapScale': mapScale,'size':imagedimensions,'format':imageformat,'rotation':rotation,'f':'pjson'}
    MapExportResp = requests.get("https://collectornew.dot.state.oh.us/arcgis/rest/services/BOUNDARIES/Boundaries/MapServer/export", params=mapdata)

	# Save the file
    file = urllib2.urlopen(MapExportResp.json()['href'])
    with open(outputname, "wb") as code:
        code.write(file.read())
    print 'Saving file {}'.format(outputname)

print 'Complete'
