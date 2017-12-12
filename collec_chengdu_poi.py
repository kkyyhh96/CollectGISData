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
                    bound = "{0},{1},{2},{3}".format(minLat, minLon, maxLat, maxLon)
                    bounds.append(bound)
        except Exception as e:
            with open("e:log.txt", 'a') as log:
                log.writelines(e)
        return bounds


# AMap API request
class AMapAPI(object):
    def __init__(self, word, bounds):
        # Your Amap api key
        self.api_key = "5892a17e4899dd11bd69d6eea7361187"
        self.word = word
        self.bounds = bounds

    # Each search request
    def search_poi(self, page_num, bound):
        params = {
            "key":self.api_key,
            "polygon":bound,
            "types":self.word,
            "offset":25,
            "page":100,

            

            "q": str(self.word),
            "page_size": 20,
            "page_num": page_num,
            "scope": 2,
            "coord_type": 1,
            "ak": self.api_key,
            "output": "json",
            "bounds": bound
        }
        try:
            r = requests.get("http://restapi.amap.com/v3/place/polygon?parameters", params)
            # Translate json file
            json_data = json.loads(r.text)
        except Exception as e:
            with open("e:log.txt", 'a') as log:
                log.writelines(e)

        # No result then next request
        if json_data['total'] == 0:
            return False
        # Have result then get the name and coordinates
        else:
            for location in json_data['results']:
                poi = POI(location['name'], location['location']['lat'], location['location']['lng'])
                poi.poi_write()
            return True

    # Get all poi data in the bound
    def get_all_poi(self):
        for bound in self.bounds:
            count = 0
            while count < 20 and self.search_poi(count, bound) == True:
                count += 1
            else:
                continue
