import json
import requests
import urllib3

def lambda_handler(event, context):
    # startTime = event["startTime"]
    # year = event["year"]
    # month = event["month"]
    # day = event["day"]
    # duration = event["duration"]
    # startMile = event["startMile"]
    # finishMile = event["finishMile"]
  
    # message = f"The startTime is {startTime} and the date is {month}-{day}-{year} the startmile was {startMile} and the finishmile was {finishMile} and the activity duration was {duration}"
    message = "through"
    # Set up API endpoint and access token
    endpoint = "https://www.strava.com/api/v3/activities"
    access_token = "fc90e8da1326cc3d0428d8874aec3525ad1902c9"
    
    # Create activity data
    activity_data = {
        "name": "My Awesome Activity",
        "type": "run",
        "start_date_local": "2023-03-27T12:00:00Z",
        "elapsed_time": 3600,
        "distance": 10000,
        "description": "A great run!",
    }

    # Upload the activity file
    files = {"file": open("testRoute.gpx", "rb")}
    response = requests.post(
        f"{endpoint}?access_token={access_token}", data=activity_data, files=files
    )
    # response = urllib3.PoolManager().request("POST", f"{endpoint}?access_token={access_token}", data=activity_data, files=files)
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": message
    #     })
    # }
  
    return response
