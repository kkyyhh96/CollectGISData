# coding:utf-8
# version:python3.5
# author:Yuhao Kang
# collect poi data from BaiduMap in Chengdu

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
            with open("log.txt", 'a') as log:
                log.writelines(e)
        return bounds


# Baidu API request
class BaiduAPI(object):
    def __init__(self, word, bounds):
        # Your baidu api key
        self.api_key = ""
        self.word = word
        self.bounds = bounds

    # Each search request
    def search_poi_first(self, bound):
        try:
            params = {
                "q": str(self.word),
                "page_size": 20,
                "page_num": 0,
                "scope": 2,
                "coord_type": 2,
                "ret_coordtype": "gcj02ll",
                "ak": self.api_key,
                "output": "json",
                "bounds": bound
            }
            try:
                r = requests.get("http://api.map.baidu.com/place/v2/search", params)
                json_data = json.loads(r.text)
                if json_data['status'] == 0:
                    return json_data['total'],json_data
            # Translate json file
            except Exception as exception:
                with open("log.txt", 'a') as log:
                    log.writelines(exception)
        except Exception as e:
            return None

    # Each search request
    def search_poi(self, page_num, bound):
        try:
            params = {
                "q": str(self.word),
                "page_size": 20,
                "page_num": page_num,
                "scope": 2,
                "coord_type": 2,
                "ret_coordtype": "gcj02ll",
                "ak": self.api_key,
                "output": "json",
                "bounds": bound
            }
            try:
                r = requests.get("http://api.map.baidu.com/place/v2/search", params)
                json_data = json.loads(r.text)
                if json_data['status'] == 0:
                    return json_data
            # Translate json file
            except Exception as exception:
                with open("log.txt", 'a') as log:
                    log.writelines(exception)
        except Exception as e:
            return None

    def decode_json(self, json_data):
        if json_data is not None:
            for location in json_data['results']:
                try:
                    poi = POI(location['name'], location['location']['lat'], location['location']['lng'],
                              location['address'])
                    type = ""
                    tag = ""
                    try:
                        type = location['detail_info']['type']
                    except Exception as e:
                        pass
                    try:
                        tag = location['detail_info']['tag']
                    except Exception as e:
                        pass
                    poi.get_type(type, tag)
                    poi.poi_write()
                except Exception as e:
                    with open("log.txt", 'a') as log:
                        log.writelines(e)

    # Get all poi data in the bound
    def get_all_poi(self):
        for bound in self.bounds:
            try:
                count, json_data = self.search_poi_first(bound)
                page_count = int(count / 20)
                self.decode_json(json_data)
                if page_count > 0:
                    for i in range(1, page_count+1):
                        try:
                            json_data = self.search_poi(count, bound)
                            self.decode_json(json_data)
                        except Exception as e:
                            with open('log.txt', 'a') as logfile:
                                logfile.writelines(e)
            except Exception as e:
                with open('log.txt', 'a') as logfile:
                    logfile.writelines(e)


class POI(object):
    def __init__(self, name, lat, lon, address):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.address = address

    def get_type(self, type="", tag=""):
        self.type = type
        self.tag = tag

    # Save in csv file
    def poi_write(self):
        try:
            with open(file_name, 'a') as file:
                file.writelines(
                    "{0},{1},{2},{3},{4},{5}\n".format(self.name, self.lat, self.lon, self.address,
                                                       self.type, self.tag))
        except Exception as e:
            with open("log.txt", 'a') as log:
                log.writelines(e)


if __name__ == '__main__':
    # Search key word
    query_word_list = ["美食", "酒店", "购物", "生活服务", "丽人", "旅游景点",
                       "休闲娱乐", "运动健身", "教育培训", "文化传媒", "医疗",
                       "汽车服务", "交通设施", "金融", "房地产", "公司企业", "政府机构"]
    for query_word in query_word_list:
        global file_name
        file_name = "{0}.csv".format(query_word)
        # Set region bound and interval
        # minLat,minLon,maxLat,maxLon,interval
        region = "30.3216,103.6,31.015,104.484"
        location = LocationDivide(region, 0.01)

        # Collect POI data
        print("Start! Key word: {0}, Region: {1}".format(query_word, region))
        try:
            baidu_search = BaiduAPI(query_word, location.compute_block())
            baidu_search.get_all_poi()
        except Exception as e:
            with open('log.txt', 'a') as logfile:
                logfile.writelines(e)
        print("End!")
