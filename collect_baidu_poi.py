# coding:utf-8
# version:python3.5
# author:Yuhao Kang
# collect poi data from BaiduMap

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
        try:
            r = requests.get("http://api.map.baidu.com/place/v2/search", params)
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


class POI(object):
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    # Save in csv file
    def poi_write(self):
        try:
            with open("e:\\poi.csv", 'a') as file:
                file.writelines("{0},{1},{2}\n".format(self.name, self.lat, self.lon))
        except Exception as e:
            with open("e:log.txt", 'a') as log:
                log.writelines(e)


if __name__ == '__main__':
    # Search key word
    query_word = "美食"

    # Set region bound and interval
    # minLat,minLon,maxLat,maxLon,interval
    region = "39.915,116.405,39.975,116.415"
    location = LocationDivide(region, 0.01)

    # Collect POI data
    print("Start! Key word: {0}, Region: {1}".format(query_word, region))
    baidu_search = BaiduAPI(query_word, location.compute_block())
    baidu_search.get_all_poi()
    print("End!")
