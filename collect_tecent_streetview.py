# coding:utf-8
# version:python3.5
# author:Yuhao Kang
# collect street view data from BaiduMap

import requests


# Baidu API request
class BaiduAPI(object):
    def __init__(self):
        # Your baidu api key
        self.api_key = "uwhciGdsgvcAvzybc6Up1S4Q"

    # Each search request
    def search_photo(self, longitude, latitude):
        params = {
            "ak": self.api_key,
            "coordtype": "wgs84ll",
            "location": "{0},{1}".format(longitude, latitude),
            "fov": 360
        }
        try:
            # Download pictures
            r = requests.get("http://api.map.baidu.com/panorama/v2", params)
            open("{0}_{1}.png".format(longitude,latitude), 'wb').write(r.content)
        except Exception as e:
            with open("e:log.txt", 'a') as log:
                log.writelines(e)


if __name__ == '__main__':
    # Read data from csv
    with open('data.csv', 'r') as data:
        lines = data.readlines()
        for line in lines:
            # Get coordinates
            longitude = line.split(',')[0]
            latitude = line.split(',')[1]
            # Get pictures
            baidu=BaiduAPI()
            baidu.search_photo(longitude,latitude)
