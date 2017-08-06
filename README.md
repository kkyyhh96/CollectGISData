# Interview demo code for Song Gao
## Collect POI Using Baidu API
I uses Baidu Place API to do this.
http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
Modify the parameter in the main function in the bottome of the code.
- Set the query key word. I recommend to follow the categories of Baidu.
http://lbsyun.baidu.com/index.php?title=lbscloud/poitags
- Set the boundary of the region. The region should be a rectangle region followed by minLat,minLon,maxLat,maxLon.
For example: region="39.915,116.405,39.975,116.415"
- Change the length of square's side, the smaller the more accuracy while slower.
For example: location = LocationDivide(region, 0.01)


## Collect Street View Using Baidu API

