def load_data(cityList, coordList, popList, distanceList):
    
    real = []
    i = 0 
    L = []
    f = open("miles.dat")
    for line in f:
        #############
        # CITY LIST #
        #############
        if ("A" <= line[0]) and (line[0] <= "Z"):
            # ADD CODE HERE to extract cityName and stateCode
            cityName = line.split(',')[0]
            stateCode = line.split(',')[1].split('[')[0]
            cityList.append(cityName + stateCode)
        ##############
        # COORD LIST #
        ##############
        if '[' in line:
            first = line.index('[')
            second = line.index(']')
            alm = line[first+1:second]
            so = alm.split(',')
            real = []
            for close in so:
                real.append(int(close))  
            coordList.append(real)
        ############
        # POP LIST #
        ############
        if ']' in line:
            hi = line.index(']')
            lo = line.index('\n')
            popList.append(int(line[hi+1:lo]))
        #################
        # DISTANCE LIST #
        #################        
        if line[0].isdigit():  
            L += line.split()
        elif line[0] == '*' and (i < 1):
            0  
        else:
            i = i + 1
            if i > 1:
                new = L[::-1]
                real = []
                for x in new:
                    real.append(int(x))
                distanceList.append(real)
                L = []
            elif i == 128:
                new = L[::-1]
                real = []
                for x in new:
                    real.append(int(x))
                distanceList.append(real)
                
def getCoordinates(cityList, coordList, name):    
    val = cityList.index(name)   
    return coordList[val]

def getPopulation(cityList, popList, name):    
    val = cityList.index(name)    
    return popList[val]

def getDistance(cityList, distanceList, name1, name2):    
    one = cityList.index(name1)
    two = cityList.index(name2)    
    if one == two:
        return 0 
    elif one > two:
        return distanceList[one][two]
    else:
        return distanceList[two][one]

def nearbyCities(cityList, distanceList, name, r):
    res = []
    n = cityList.index(name)
    i=0
    while i < n:
        if float(distanceList[n][i]) <= r:
            res.append(cityList[i])     
        i +=1
    j = n + 1
    while j < len(cityList):
        if float(distanceList[j][n]) <= r:
            res.append(cityList[j])           
        j += 1
    return res 


def numNotServed(served, cityList, distanceList, name, r):
    #this will count how many cities the select city can serve 
    count = 0
    #this checks the length of nearby cities, or the amount of nearby cities 
    val = len(nearbyCities(cityList, distanceList, name, r))
    if served[cityList.index(name)] == False:
        val+=1    
    #this will let us check the nearby cities for 
    nearby = nearbyCities(cityList, distanceList, name, r)
    #this loop checks nearby for any cities that have already been served 
    for x in nearby:
        ind = cityList.index(x)
        if served[ind] == True:
            count += 1
    #this takes the amount of nearby cities of the city, and subtracts the amount of cities that have already been served 
    real = val - count
    return real
    
def nextFacility(served, cityList, distanceList, r):
    #find the city that serves the most cities 
    #this is set to -1 so we can account for when no cities are being served anymore 
    maxCitiesToServe = 0
    nextBest = None
    #loop to check each city in cityList
    for name in cityList:
        #checks to see if the cities served is larger than the current max, by the end of the loop, it will 
        if numNotServed(served, cityList, distanceList, name, r) > maxCitiesToServe:
            maxCitiesToServe = numNotServed(served, cityList, distanceList, name, r)
            nextBest = name 
    return nextBest
       
def locateFacilities(cityList, distanceList, r):
    #initialize served 
    served = [False] * len(cityList)
    #initialize the result 
    res = []
    #first facility 
    facility = nextFacility(served, cityList, distanceList, r)
    while not all(served): 
        if facility == None:
            break
        #append the best facility
        res.append(facility)
        #get a list the nearby cities to the facility 
        nearby = nearbyCities(cityList, distanceList, facility, r)
        #assign each city in nearby to "served"
        for x in nearby:
            ind = cityList.index(x)
            served[ind] = True
        #assign the facility city to served 
        facInd = cityList.index(facility)
        served[facInd] = True 
        #get the next facility 
        facility = nextFacility(served, cityList, distanceList, r)
    return res
    
def display(res, cityList, distanceList, coordList, r):
        
    servedCities = [] 
    for x in res:
        servedCities += [[]]
    
    #open file, first 3 lines

    f = open('visualization'+str(r)+'.kml','w')
    
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n\n')
    
    #icons for facilities
    f.write('<Style id="facilityIcon">')
    f.write('<IconStyle>')
    f.write('<Icon>')
    f.write('<href>https://cdn-icons-png.flaticon.com/512/2942/2942544.png</href>')
    f.write('</Icon>')
    f.write('</IconStyle>')
    f.write('</Style>')
    
    #icons for normal cities
    f.write('<Style id="cityIcon">')
    f.write('<IconStyle>')
    f.write('<Icon>')
    f.write('<href>https://cdn-icons-png.flaticon.com/512/2451/2451728.png</href>')
    f.write('</Icon>')
    f.write('</IconStyle>')
    f.write('</Style>')    
    
    # Placemark for every city that is a facility 
    
    for i in range(len(res)):
        f.write('<Placemark>\n')
        f.write('<styleUrl>#facilityIcon</styleUrl>')
        # string concatenation
        f.write('<name>'+res[i]+'</name>\n')
        ind = cityList.index(res[i])
        f.write('<Point>\n')
        # getting correct version of coordinates
        formattedLong = '-'+str(coordList[ind][1])[:-2]+'.'+str(coordList[ind][1])[-2:]
        formattedLat = str(coordList[ind][0])[:-2]+'.'+str(coordList[ind][0])[-2:]
        f.write('<coordinates>'+formattedLong+','+formattedLat+',0</coordinates>\n')
        f.write('</Point>\n')
        f.write('</Placemark>\n')
    
    i = 0
    while i < len(cityList):
        j = 0
        minDis = getDistance(cityList, distanceList, cityList[i], res[j])
        minInd = 0
        while j < len(res):
            distance = getDistance(cityList, distanceList, cityList[i], res[j])
            if distance == minDis:
                minInd = j
            elif distance < minDis:
                minDis = distance
                minInd = j
            j += 1
        servedCities[minInd] = servedCities[minInd] + [cityList[i]]
        i += 1
        
    # write line, im going to make the further distances a darker shade
    f.write('<Style id="yellowLine">')
    f.write('<LineStyle>')
    f.write('<width>1.5</width>')
    # hex value for a color
    f.write('<color>ff00ffff</color>')
    f.write('</LineStyle>')
    f.write('</Style>')       
    
    f.write('<Style id="orangeLine">')
    f.write('<LineStyle>')
    f.write('<width>1.5</width>')
    # hex value for a color
    f.write('<color>ff0080ff</color>')
    f.write('</LineStyle>')
    f.write('</Style>')       
    
    f.write('<Style id="redLine">')
    f.write('<LineStyle>')
    f.write('<width>1.5</width>')
    # hex value for a color
    f.write('<color>ff0000ff</color>')
    f.write('</LineStyle>')
    f.write('</Style>')           
    
    i = 0
    while i < len(res):
        for x in servedCities[i]:
            if x in res:
                continue 
            
            f.write('<Placemark>\n')
            f.write('<styleUrl>#cityIcon</styleUrl>')
            # string concatenation
            f.write('<name>'+x+'</name>\n')
            ind = cityList.index(x)
            f.write('<Point>\n')
            # getting correct version of coordinates
            formattedLong = '-'+str(coordList[ind][1])[:-2]+'.'+str(coordList[ind][1])[-2:]
            formattedLat = str(coordList[ind][0])[:-2]+'.'+str(coordList[ind][0])[-2:]
            f.write('<coordinates>'+formattedLong+','+formattedLat+',0</coordinates>\n')
            f.write('</Point>\n')
            f.write('</Placemark>\n') 

            facInd = cityList.index(res[i])
            cityInd = cityList.index(x)
            facformattedLong = '-'+str(coordList[facInd][1])[:-2]+'.'+str(coordList[facInd][1])[-2:]
            facformattedLat = str(coordList[facInd][0])[:-2]+'.'+str(coordList[facInd][0])[-2:]        
            cityformattedLong = '-'+str(coordList[cityInd][1])[:-2]+'.'+str(coordList[cityInd][1])[-2:]
            cityformattedLat = str(coordList[cityInd][0])[:-2]+'.'+str(coordList[cityInd][0])[-2:]
            if getDistance(cityList, distanceList, res[i], x) < 250:
                f.write('<Placemark>\n')
                f.write('<name>'+x+'</name>\n')
                f.write('<description>Line between ' + x + ' and ' + res[i]+'</description>\n')
                f.write('<styleUrl>#yellowLine</styleUrl>')
                f.write('<LineString>')
                f.write('<coordinates>'+cityformattedLong+','+cityformattedLat+',0,' + facformattedLong+','+facformattedLat+',0</coordinates>')
                f.write('</LineString>')
                f.write('</Placemark>') 
            elif getDistance(cityList, distanceList, res[i], x) < 650:
                f.write('<Placemark>\n')
                f.write('<name>'+x+'</name>\n')
                f.write('<description>Line between ' + x + ' and ' + res[i]+'</description>\n')
                f.write('<styleUrl>#orangeLine</styleUrl>')
                f.write('<LineString>')
                f.write('<coordinates>'+cityformattedLong+','+cityformattedLat+',0,' + facformattedLong+','+facformattedLat+',0</coordinates>')
                f.write('</LineString>')
                f.write('</Placemark>')
            else:
                f.write('<Placemark>\n')
                f.write('<name>'+x+'</name>\n')
                f.write('<description>Line between ' + x + ' and ' + res[i]+'</description>\n')
                f.write('<styleUrl>#redLine</styleUrl>')
                f.write('<LineString>')
                f.write('<coordinates>'+cityformattedLong+','+cityformattedLat+',0,' + facformattedLong+','+facformattedLat+',0</coordinates>')
                f.write('</LineString>')
                f.write('</Placemark>')    
        i += 1
    
    #ending
    f.write('</Document>\n')
    f.write('</kml>')

# main program
cityList = []
coordList = []
popList = []
distanceList = []

loadData(cityList, coordList, popList, distanceList)

res = locateFacilities(cityList, distanceList, 300)
display(res, cityList, distanceList, coordList, 300)
res = locateFacilities(cityList, distanceList, 800)
display(res, cityList, distanceList, coordList, 800)