import json
import os
import boto3
import urllib3
from io import BytesIO
import pacificCrestTrailMileMarkers



def lambda_handler(event, context):
    startTime = event["startTime"]
    year = event["year"]
    month = event["month"]
    day = event["day"]
    totalTime = event["duration"]
    startMile = event["startMile"]
    finishMile = event["finishMile"]
    authCode = event["authCode"]
  
    message = f"The startTime is {startTime} and the date is {month}-{day}-{year} the startmile was {startMile} and the finishmile was {finishMile} and the activity duration was {totalTime}"
    print(message)
    
    http = urllib3.PoolManager()

    client_id = '98457'
    client_secret = '13e74e5deb9db6a8b61af49514e72f93158315de'
    code = authCode
    # code ='e3fdd5fa180a79f33a77b4fd442ef7086d1fbdb8'
    grant_type = 'authorization_code'
    
    urlToken = 'https://www.strava.com/api/v3/oauth/token'
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': grant_type
    }
    
    
    
    
    
    # READING IN FILE FROM S3 BUCKET
    # create an S3 client
    s3 = boto3.client('s3')
    
    # define the bucket and file name
    bucket_name = 'baconmaps'
    file_name = 'fullPCT.gpx'
    
    # download the file from S3 to a temporary file in the /tmp directory
    with open('/tmp/' + file_name, 'wb') as f:
        s3.download_fileobj(bucket_name, file_name, f)
    
    # read the contents of the file
    with open('/tmp/' + file_name, 'rb') as f:
        gpx_data = f.read()
    
    
    
    
    
    
    
    
    
    # create new gpx file with data
    
    # getting time
    fullTime = "<time>" + year + "-" + month + "-" + day + "T"
    
    # getting coords of start and finish
    startCoordsLat = str(pacificCrestTrailMileMarkers.coordsFuncLat(int(startMile)))
    startCoordsLon = str(pacificCrestTrailMileMarkers.coordsFuncLon(int(startMile)))
    finishCoordsLat = str(pacificCrestTrailMileMarkers.coordsFuncLat(int(finishMile)))
    finishCoordsLon = str(pacificCrestTrailMileMarkers.coordsFuncLon(int(finishMile)))
    
    print("start is lat: "+startCoordsLat+" and lon: "+startCoordsLon)
    print("finish is lat: "+finishCoordsLat+" and lon: "+finishCoordsLon)
    
    # editing gpx file
    full = ""
    checker = "/ele"
    count = 0
    countStart = 0
    countFinish = 0
    
    # get line number for start and finish
    
    # line starts
    with open("/tmp/fullPCT.gpx", "r") as myFile:
        for data in myFile:
            findLat = data.find(startCoordsLat[:6])
            findLon = data.find(startCoordsLon[:7])
            if findLat != -1 and findLon != -1:
                print("found")
                print(startCoordsLat, "is start coords Lat")
                print(startCoordsLon, "is start coords Lon")
                print(data, "is data\n\n\n")
                break
            countStart += 1
    
    # line for finish
    with open("/tmp/fullPCT.gpx", "r") as myFile1:
        for data in myFile1:
            findLat2 = data.find(finishCoordsLat[:6])
            findLon2 = data.find(finishCoordsLon[:7])
            if findLat2 != -1 and findLon2 != -1:
                print("found")
                print(finishCoordsLat, "is finish coords Lat")
                print(finishCoordsLon, "is finish coords Lon")
                print(data, "is data\n\n\n")
                break
            countFinish += 1
            
            
            
            
    front = ""
    full=""
    print("count start is: "+str(countStart))
    print("count finish is: "+str(countFinish))
    var_start = countStart-1
    var_fin = countFinish+30
    totalLines = var_fin-var_start
    print("total Lines is " + str(totalLines))
    print("total lines post division is " + str(totalLines))
    increments = int(totalTime)//totalLines
    print("increments is " + str(increments))
    currentHour = int(startTime)
    currentMinute = 0
    currentSecond = 0
    
    with open("/tmp/fullPCT.gpx", 'r') as myFile3:
        data = myFile3.readlines()
        for line in data:
            if count<17:
                front += line
            elif var_start<count and count<var_fin:
                full += line[:-9]
                found = line.find(checker)
                if found != -1:
                    tempHour = str(currentHour)
                    tempMinute = str(currentMinute)
                    tempSecond = str(currentSecond)
                    if int(currentHour) < 10:
                        tempHour = "0" + str(currentHour)
                    if int(currentMinute) < 10:
                        tempMinute = "0" + str(currentMinute)
                    if int(currentSecond) < 10:
                        tempSecond = "0" + str(currentSecond)
                    full += fullTime + tempHour + ":" + tempMinute + ":" + tempSecond + "Z</time></trkpt>\n"
                    currentSecond += increments
                    if currentSecond > 59:
                        currentMinute += 1
                        currentSecond -= 60
                    if currentMinute > 59:
                        currentHour += 1
                        currentMinute -= 60
            elif count > 88293:
                full += line
            count += 1
    
    full = front + full + "</trkseg></trk></gpx>"
    # print("full is: ")
    # print(full)
    with open("/tmp/fullPCT.gpx", 'w+') as newFile4:
        newFile4.write(full)
        # gpx_data = newFile4.read()
        # print("gpx data is")
        # print(gpx_data)
        # print("gpx_data complete")
    with open("/tmp/fullPCT.gpx", 'r') as newFile5:
        gpx_data=newFile5.read()
        # print(gpx_data)
            

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        response = http.request('POST', urlToken, headers=headers, body=json.dumps(body).encode('utf-8'))
        response_data = json.loads(response.data.decode('utf-8'))
        strava_access_token = response_data['access_token']
        print("access token is: "+strava_access_token)
        
        print("b4 last print")
        print(gpx_data)
        print("last print")
        
        # READING IN FILE FROM MY S3 BUCKET
        # # create an S3 client
        # s3 = boto3.client('s3')
        
        # # define the bucket and file name
        # bucket_name = 'baconmaps'
        # file_name = 'newFileHike.gpx'
        
        # # download the file from S3 to a temporary file in the /tmp directory
        # with open('/tmp/' + file_name, 'wb') as f:
        #     s3.download_fileobj(bucket_name, file_name, f)
        
        # # read the contents of the file
        with open('/tmp/fullPCT.gpx', 'r') as f:
            gpx_data = f.read()
        
        
            # print("gpx data is this here:")
            # print(gpx_data)
        
        # create the request headers
        headers = {
            'Authorization': f'Bearer {strava_access_token}'
        }
        # print(gpx_data)
        # print("above is gpx data")
        # create the data payload
        data = {
            'name':'fullPCT.gpx',
            'file': (file_name, gpx_data, 'application/gpx+xml')
        }
        
        # send the request
        response = http.request(
            method='POST',
            url='https://www.strava.com/api/v3/uploads?data_type=gpx',
            headers=headers,
            fields=data
        )
        
        # print the response
        print(response.data.decode())

    
    return message
