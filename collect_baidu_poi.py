# coding:utf-8
# version:python3.5
# author:Yuhao Kang
# collect poi data from BaiduMap

import requests
import json


# Research region
class LocationDivide(object):
    def __init__(self, bound, size):
        # maxLat,minLon,minLat,maxLon
        self.maxLat = float(str(bound).split(',')[0])
        self.minLon = float(str(bound).split(',')[1])
        self.minLat = float(str(bound).split(',')[2])
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
        for i in range(0, lat_count):
            for j in range(0, lon_count):
                # maxLat,minLon,minLat,maxLon
                maxLat = self.maxLat - i * self.size
                minLon = self.minLon + i * self.size
                minLat = self.maxLat - (i + 1) * self.size
                if minLat < self.minLat:
                    minLat = self.minLat
                maxLon = self.minLon + (i + 1) * self.size
                if maxLon > self.maxLon:
                    maxLon = self.maxLon
                bound = "{0},{1},{2},{3}".format(maxLat, minLon, minLat, maxLon)
                bounds.append(bound)
        return bounds


# Baidu API request
class BaiduAPI(object):
    def __init__(self, word, bounds):
        # Your baidu api key
        self.api_key = "uwhciGdsgvcAvzybc6Up1S4Q"
        self.word = word
        self.bounds = bounds

    # Each search request
    def search_poi(self, page_num, bound):
        params = {
            "q": str(self.word),
            "page_size": 20,
            "page_num": page_num,
            "scope": 2,
            "coord_type": 1,
            "ak": self.api_key,
            "output": "json",
            "bounds": bound
        }
        r = requests.get("http://api.map.baidu.com/place/v2/search", params)
        json_data=json.load(r.text)
        for poi in json_data:
            if poi['total']==0:
                return False
            else:
                for location in poi['results']:
                    poi=POI(location['name'],location['location']['lat'],location['location']['lon'])
                    poi.poi_write()
                return True


    def get_all_poi(self):
        count=0
        for bound in self.bounds:
            while self.search_poi(count,bound)== True:
                count+=1
            else:
                continue



class POI(object):
    def __init__(self,name,lat,lon):
        self.name=name
        self.lat=lat
        self.lon=lon

    def poi_write(self):
        with open("e:\\poi.csv",'a') as file:
            file.writelines("{0},{1},{2}".format(self.name,self.lat,self.lon))

if __name__ == '__main__':
    # Search key word
    query_word = "美食"

    # Set region bound
    # maxLat,minLon,minLat,maxLon
    location = LocationDivide("39.975,116.405,39.915,116.415", 0.05)
    baidu_search = BaiduAPI(query_word, location.compute_block())
