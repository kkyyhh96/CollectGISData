# coding:utf-8
# version:python3.5
# author:Yuhao Kang
# collect chengdu poi data from AMap

import json

import requests


# Research region
class LocationDivide(object):
    def __init__(self, bound, size):
        # minLat,minLon,maxLat,maxLon
        self.minLat = float(str(bound).split(',')[0])
        self.minLon = float(str(bound).split(',')[1])
        self.maxLat = float(str(bound).split(',')[2])
        self.maxLon = float(str(bound).split(',')[3])
        self.size = size

    def compute_block(self):
        if (self.maxLat - self.minLat) % self.size == 0:
            lat_count = (self.maxLat - self.minLat) / self.size
        else:
            lat_count = (self.maxLat - self.minLat) / self.size + 1
        if (self.maxLon - self.minLon) % self.size == 0:
            lon_count = (self.maxLon - self.minLon) / self.size
        else:
            lon_count = (self.maxLon - self.minLon) / self.size + 1
        bounds = []
        lat_count = int(lat_count)
        lon_count = int(lon_count)

        try:
            for i in range(0, lat_count):
                for j in range(0, lon_count):
                    # maxLat,minLon,minLat,maxLon
                    minLat = self.minLat + i * self.size
                    minLon = self.minLon + j * self.size
                    maxLat = self.minLat + (i + 1) * self.size
                    if maxLat > self.maxLat:
                        maxLat = self.maxLat
                    maxLon = self.minLon + (j + 1) * self.size
                    if maxLon > self.maxLon:
                        maxLon = self.maxLon
                    # minLat,minLon,maxLat,maxLon
                    bound = "{0},{1}|{2},{3}".format(minLon,maxLat,maxLon,minLat)
                    bounds.append(bound)
        except Exception as e:
            with open("log.txt", 'a') as log:
                log.writelines(e)
        return bounds


# AMap API request
class AMapAPI(object):
    def __init__(self, search_type, bounds):
        # Your Amap api key
        self.api_key = "66be70cd5f865446b870937f042c8e74"
        # self.api_key = "5892a17e4899dd11bd69d6eea7361187"
        self.type = search_type
        self.bounds = bounds

    # Each search request
    def search_poi(self, page_num, bound):
        params = {
            "key": self.api_key,
            "polygon": bound,
            "types": self.type,
            "offset": 25,
            "page": page_num,
            "output": "JSON",
            "extensions": "all"
        }
        try:
            r = requests.get("http://restapi.amap.com/v3/place/polygon?parameters", params)
            # Translate json file
            json_data = json.loads(r.text)
        except Exception as e:
            with open("log.txt", 'a') as log:
                log.writelines(e)

        # No result then next request
        if json_data['count'] == "0":
            return False
        # Have result then get the name and coordinates
        else:
            for json_text_poi in json_data['pois']:
                poi = POI(json_text_poi)
                poi.poi_write()
            if len(json_data['pois'])<25:
                return False
            return True

    # Get all poi data in the bound
    def get_all_poi(self):
        for bound in self.bounds:
            count = 0
            if count >= 99:
                try:
                    with open(r"poi.csv", 'a') as file:
                        file.writelines("Exceed:{0}\n".format(bound))
                except Exception as e:
                    with open(r"log.txt", 'a') as log:
                        log.writelines(e)
            while count < 100 and self.search_poi(count, bound) == True:
                count += 1
            else:
                continue


class POI(object):
    def __init__(self, json_text):
        self.name = json_text['name']
        self.lon = json_text['location'].split(',')[0]
        self.lat = json_text['location'].split(',')[1]
        self.type = json_text['type']
        self.typecode = json_text['typecode']
        self.address = json_text['address']
        self.pcode = json_text['pcode']
        self.pname = json_text['pname']
        self.citycode = json_text['citycode']
        self.cityname = json_text['cityname']
        self.adcode = json_text['adcode']
        self.adname = json_text['adname']

    # Save in csv file
    def poi_write(self):
        try:
            with open(r"poi.csv", 'a') as file:
                file.writelines("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(
                    self.name, self.lat, self.lon, self.type, self.typecode, self.address, self.pcode,
                    self.pname, self.citycode, self.cityname, self.adcode, self.adname))
        except Exception as e:
            with open(r"log.txt", 'a') as log:
                log.writelines(e)


if __name__ == '__main__':
    # Search key word
    query_type = "公共设施"

    # Set region bound and interval
    # minLat,minLon,maxLat,maxLon,interval
    # (103.5998, 104.483069)(30.321640000000002, 31.01437)
    region = "30.3216,103.6,31.015,104.484"
    location = LocationDivide(region, 0.01)

    # Collect POI data
    print("Start! Key word: {0}, Region: {1}".format(query_type, region))
    amap_search = AMapAPI(query_type, location.compute_block())
    amap_search.get_all_poi()
    print("End!")
