import json
import os
import boto3
import urllib3
from io import BytesIO



def lambda_handler(event, context):
    # startTime = event["startTime"]
    # year = event["year"]
    # month = event["month"]
    # day = event["day"]
    # duration = event["duration"]
    # startMile = event["startMile"]
    # finishMile = event["finishMile"]
  
    # message = f"The startTime is {startTime} and the date is {month}-{day}-{year} the startmile was {startMile} and the finishmile was {finishMile} and the activity duration was {duration}"
    message = "passed all TTYSTSYTSTS"
    

    http = urllib3.PoolManager()
    http = urllib3.PoolManager()

    client_id = '98457'
    client_secret = '13e74e5deb9db6a8b61af49514e72f93158315de'
    code = 'c9bf98a1fba90a15106851d026a645d4e0ec6bb9'
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
    
    response = http.request('POST', urlToken, headers=headers, body=json.dumps(body).encode('utf-8'))
    response_data = json.loads(response.data.decode('utf-8'))
    strava_access_token = response_data['access_token']
    print("access token is: "+strava_access_token)
    
    # create an S3 client
    s3 = boto3.client('s3')
    
    # define the bucket and file name
    bucket_name = 'baconmaps'
    file_name = 'newFile1.gpx'
    
    # download the file from S3 to a temporary file in the /tmp directory
    with open('/tmp/' + file_name, 'wb') as f:
        s3.download_fileobj(bucket_name, file_name, f)
    
    # read the contents of the file
    with open('/tmp/' + file_name, 'rb') as f:
        gpx_data = f.read()
    
    print(gpx_data)
    
    # create the request headers
    headers = {
        'Authorization': f'Bearer {strava_access_token}'
    }
    
    # create the data payload
    data = {
        'name':'newFile1.gpx',
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


    
    
    
    
    
    
    
    # name = "My Manual Activity"
    # type = "Run"
    # start_date_local = "2023-03-27T14:20:00-07:00"
    # elapsed_time = "200"
    # description = "My activity description"
    # distance = "1000"
    
    # http = urllib3.PoolManager()
    # url = "https://www.strava.com/api/v3/activities?name="+name+"&type="+type+"&start_date_local="+start_date_local+"&elapsed_time="+elapsed_time+"&description="+description+"&distance="+distance
    # # https://www.strava.com/api/v3/activities?name='+NAME+'&type='+TYPE+'&sport_type='+TYPE+'&start_date_local='+SET_TIME+'&elapsed_time='+MOVE_TIME+'&description='+STRAVA_DESCRIPTION+'&distance='+ACTIVITY_DIST+'&train
    # url_athlete = "https://www.strava.com/api/v3/athlete"

    # # data = {
    # #     "name": name,
    # #     "type": type,
    # #     "start_date_local": start_date_local,
    # #     "elapsed_time": elapsed_time,
    # #     "description": description,
    # #     "distance": distance,
    # # }
    # headers = {
    #     "Authorization": f"Bearer {strava_access_token}"
    # }
    
    # # encoded_data = json.dumps(data).encode('utf-8')
    # response = http.request('POST', url, headers=headers)
    # # response = http.request('GET', url_athlete, headers=headers)
    # print(response.status)
    # print(response.data.decode('utf-8'))

    
    return message
