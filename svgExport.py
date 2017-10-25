import requests, math

NLFID = 'SFRAIR00270**N'
CTL_BEGIN = 0
CTL_END = 3

while CTL_BEGIN <= 6:

    imagedimensions = '1200,500'
    imageformat = 'png'
    outputname = '{}_{}_{}.{}'.format(NLFID.replace('*','-'),str(CTL_BEGIN).replace('.','-'),str(CTL_END).replace('.','-'),imageformat)

    routePayload ={'routeId':NLFID,'fromMeasure':CTL_BEGIN,'toMeasure':CTL_END,'f': 'pjson'} # Set the input values for ODOT LRS Tools.

    DynSegResp = requests.get("http://collectornew.dot.state.oh.us/arcgis/rest/services/OdotLrsTools/LRS_2015_StateAndRamps/MapServer/exts/OdotDynSegTools/CountyRouteBetweenMs", params=routePayload)

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
    #		print rotation
    #       print dist

            xmin = (min(xlist) + max(xlist))/2-(dist/2)
            xmax = (min(xlist) + max(xlist))/2+(dist/2)
            # image dimension ratio
            ratio = float(imagedimensions.split(',')[0])/float(imagedimensions.split(',')[1])
            ymin = (min(ylist) + max(ylist))/2-(dist/ratio/2)
            ymax = (min(ylist) + max(ylist))/2+(dist/ratio/2)
            # create a bufferer around bbox
            boundingbox = '{0},{1},{2},{3}'.format(xmin*0.99998,ymin*0.99998,xmax*1.00002,ymax*1.00002)
    #       print boundingbox

            mapPayload = {'bbox':boundingbox,'size':imagedimensions,'format':imageformat,'rotation':rotation,'f':'image', 'format':'png'}
            MapExportResp = requests.get("https://collectornew.dot.state.oh.us/arcgis/rest/services/BOUNDARIES/Boundaries/MapServer/export", params=mapPayload)
            #  write out to file
            with open("export/"+outputname, "wb") as code:
                code.write(MapExportResp.content)
                print 'Saving file {}'.format(outputname)
    CTL_BEGIN += 3
    CTL_END += 3
print 'Complete'
