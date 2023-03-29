import json
import os
import boto3
import urllib3
from io import BytesIO


mileMarkers = [
    [0,32.58971,-116.46696],
    [0.5,32.59585,-116.46671],
    [1,32.60058,-116.47008],
    [1.5,32.60587,-116.47302],
    [2,32.60531,-116.47906],
    [2.5,32.60728,-116.48308],
    [3,32.607,-116.48882],
    [3.5,32.60604,-116.49273],
    [4,32.60603,-116.49679],
    [4.5,32.60708,-116.49982],
    [5,32.60907,-116.50446],
    [5.5,32.60956,-116.50703],
    [6,32.6147,-116.50759],
    [6.5,32.61931,-116.50776],
    [7,32.62333,-116.50734],
    [7.5,32.62792,-116.51084],
    [8,32.62952,-116.51533],
    [8.5,32.62662,-116.51669],
    [9,32.62483,-116.52018],
    [9.5,32.62848,-116.52375],
    [10,32.6344,-116.52569]
]

def coordsFuncLat(mileMarker):
    i = int(2*mileMarker)
    coordsLat = mileMarkers[i][1]
    return coordsLat

def coordsFuncLon(mileMarker):
    i = int(2*mileMarker)
    coordsLon = mileMarkers[i][2]
    return coordsLon
