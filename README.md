# Interview demo code for Song Gao
## Collect POI Using Baidu API
I use Baidu Place API to do this.
http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi
### Usage
Modify the parameter in the main function in the bottom of the code.
- Set the query key word. I recommend to follow the categories of Baidu.
http://lbsyun.baidu.com/index.php?title=lbscloud/poitags
- Set the boundary of the region. The region should be a rectangle region followed by minLat,minLon,maxLat,maxLon.
For example: region="39.915,116.405,39.975,116.415"
- Change the length of square's side, the smaller the more accuracy while slower.
For example: location = LocationDivide(region, 0.01)


## Collect Street View Using Baidu API
I use an arctoolbox: CreatePointsLines.tbx to do this.
### Usage
- Import network / road polyline data in ArcGIS.
- Use CreatePointsLines toolbox to generate points along with the polylines with equal distance.
- Compute points' coordinates and then export them into a csv file.
- Set the csv file path to download the pictures.
